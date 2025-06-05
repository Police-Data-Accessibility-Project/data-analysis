from functools import wraps
from operator import and_
from typing import List, Dict

from environs import Env
from sqlalchemy import select, update, or_, Select, func, exists, literal, literal_column, Column, ColumnElement, cast, \
    Float
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from src.db.dtos.input.url_annotations import URLAnnotationsInput
from src.db.dtos.labeled_data_frame import LabeledDataFrame
from src.db.dtos.output.url import URLOutput
from src.db.enums import ErrorType
from src.db.models.core import URL, URLFullHTML, URLError, URLCompressedHTML, URLAnnotations, HTMLBagOfWords
from src.db.df_labels.bag_of_words import BagOfWordsBaseLabels
from src.nlp_processor.families.registry.instances import FAMILY_REGISTRY
from src.nlp_processor.jobs.enums import HTMLBagOfWordsJobType
from src.nlp_processor.jobs.identifiers.base import JobIdentifierBase
from src.nlp_processor.jobs.mapper.map import map_job_result_to_models
from src.nlp_processor.jobs.result.base import JobResultBase
from src.nlp_processor.run_manager.check_query_builder.core import CheckQueryBuilder
from src.nlp_processor.set.context import SetContext
from src.nlp_processor.set.state import SetState
from src.utils.compression import decompress_html, compress_html
import polars as pl

def get_postgres_connection_string():
    env = Env()
    env.read_env()
    user = env.str("POSTGRES_USER")
    password = env.str("POSTGRES_PASSWORD")
    host = env.str("POSTGRES_HOST")
    port = env.str("POSTGRES_PORT")
    database = env.str("POSTGRES_DB")

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

class DatabaseClient:

    def __init__(self):
        db_url = get_postgres_connection_string()
        self.engine = create_async_engine(
            url=db_url,
            echo=False,
        )
        self.session_maker = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    def compile(self, query):
        return query.compile(self.engine, compile_kwargs={"literal_binds": True})

    @staticmethod
    def session_manager(method):
        """Decorator to manage async session lifecycle."""

        @wraps(method)
        async def wrapper(self, *args, **kwargs):
            # Check if a session was passed in via kwargs
            existing_session: AsyncSession | None = kwargs.get("session")

            if existing_session is not None:
                # If session is already provided, use it directly
                return await method(self, *args, **kwargs)

            # Otherwise, manage session lifecycle internally
            async with self.session_maker() as session:
                async with session.begin():
                    try:
                        kwargs["session"] = session
                        result = await method(self, *args, **kwargs)
                        return result
                    except Exception as e:
                        await session.rollback()
                        raise e

        return wrapper

    @session_manager
    async def execute_all(self, session: AsyncSession, query: Select):
        result = await session.execute(query)
        return result.all()

    @session_manager
    async def execute_one(self, session: AsyncSession, query: Select):
        result = await session.execute(query)
        return result.one_or_none()

    @session_manager
    async def execute_scalar(self, session: AsyncSession, query: Select):
        result = await session.execute(query)
        return result.scalar()

    @session_manager
    async def add_urls(self, session: AsyncSession, urls: list[str]):
        for url in urls:
            url_object = URL(url=url)
            session.add(url_object)

    @session_manager
    async def add_html(self, session: AsyncSession, url_id: int, html: str):
        url_full_html = URLFullHTML(
            url_id=url_id,
            html=html
        )
        session.add(url_full_html)
        url_compressed_html = URLCompressedHTML(
            url_id=url_id,
            compressed_html=compress_html(html)
        )
        session.add(url_compressed_html)

    async def get_urls_without_response_codes(self) -> list[URLOutput]:
        query = (
            select(
                URL.id,
                URL.url,
            )
            .where(URL.response_code.is_(None))
        )
        raw_results = await self.execute_all(query)
        return [URLOutput(id=id_, url=url) for id_, url in raw_results]

        return [URLOutput(id=id_, url=url) for id_, url in raw_results]

    @session_manager
    async def add_url_error(
        self,
        session: AsyncSession,
        url_id: int,
        error: str,
        error_type: ErrorType,
    ):
        url_error = URLError(
            url_id=url_id,
            error_type=error_type,
            error=error
        )
        session.add(url_error)

    @session_manager
    async def update_response_code(self, session: AsyncSession, url_id: int, response_code: int):
        await session.execute(
            update(URL)
            .where(URL.id == url_id)
            .values(response_code=response_code)
        )

    @session_manager
    async def get_run_jobs(
        self,
        session: AsyncSession,
        job_ids: List[JobIdentifierBase]
    ) -> List[JobIdentifierBase]:
        """
        Get the set of jobs whose existence should be checked for all valid URLs in the database
        :param session:
        :param job_ids:
        :return:
        """
        builder = CheckQueryBuilder(job_ids)
        subqs = []
        for job_id in builder.job_ids:
            subq = builder.build_global_subquery(job_id)
            subqs.append(subq)
        query = select(*subqs)

        execution_result = await session.execute(query)
        row = execution_result.mappings().one_or_none()

        missing_jobs = []
        for label in builder.get_all_labels():
            any_url_missing_job = row[label]
            if any_url_missing_job:
                job_id = builder.get_job_id_from_label(label)
                missing_jobs.append(job_id)

        return missing_jobs


    @session_manager
    async def get_all_url_sets(
        self,
        session: AsyncSession,
        job_ids: List[JobIdentifierBase]
    ) -> List[SetState]:

        if len(job_ids) == 0:
            return None
        builder = CheckQueryBuilder(job_ids)
        sqs = builder.get_flag_select_subqueries()
        select_statements = [sq.select for sq in sqs]
        query = select(
            URL.id,
            URL.url,
            *select_statements,
        ).join(
            URLCompressedHTML
        )

        # Outer join for every family with jobs present
        query = builder.add_cte_outer_joins(query, sqs)

        query = query.where(
            or_(
                *select_statements
            )
        )

        execution_result = await session.execute(query)
        row = execution_result.mappings().all()

        set_states = []
        for row in row:
            set_jobs = []
            for label in builder.get_all_labels():
                url_missing_job = row[label]
                if url_missing_job:
                    job_id = builder.get_job_id_from_label(label)
                    set_jobs.append(job_id)

            set_states.append(SetState(
                context=SetContext(
                    url_info=URLOutput(
                        id=row["id"],
                        url=row["url"],
                    ),
                    html=None,
                ),
                job_ids=set_jobs
            ))
        return set_states

    @session_manager
    async def upload_jobs_for_set(
        self,
        session: AsyncSession,
        url_id: int,
        job_results: List[JobResultBase]
    ):

        all_models = []
        for job_result in job_results:
            family_type = job_result.job_id.family
            mapper = FAMILY_REGISTRY.get_mapper_class(family_type)
            models = await map_job_result_to_models(
                job_result=job_result,
                mapper_class=mapper,
                url_id=url_id,
                session=session
            )
            all_models.extend(models)

        session.add_all(all_models)

    async def get_url_url_id_map(self, session: AsyncSession) -> Dict[str, int]:
        execution_result = await session.execute(
            select(
                URL.id,
                URL.url,
            )
        )
        raw_results = execution_result.all()
        return {url: id_ for id_, url in raw_results}

    @session_manager
    async def get_html_for_url(
        self,
        session: AsyncSession,
        url_id: int
    ) -> str:
        query = (
            select(URLCompressedHTML.compressed_html)
            .where(URLCompressedHTML.url_id == url_id)
        )
        execution_result = await session.execute(query)
        row = execution_result.mappings().one_or_none()
        if row is None:
            return None
        return decompress_html(row["compressed_html"])


    @session_manager
    async def add_annotations(
        self,
        session: AsyncSession,
        annotations: List[URLAnnotationsInput]
    ):
        uui_map = await self.get_url_url_id_map(session)

        for annotation in annotations:
            url_id = uui_map[annotation.url]

            url_annotations = URLAnnotations(
                url_id=url_id,
                relevant=annotation.relevant,
                record_type_fine=annotation.record_type_fine,
                record_type_coarse=annotation.record_type_coarse
            )
            session.add(url_annotations)

    @session_manager
    async def get_bag_of_words_for_ml(
        self,
        session: AsyncSession,
        bag_of_words_type: HTMLBagOfWordsJobType = HTMLBagOfWordsJobType.ALL_WORDS,
        top_n_words: int = 1000,
        min_doc_term_threshold: int = 100
    ) -> LabeledDataFrame[BagOfWordsBaseLabels]:

        # CTE for all URLs with bag of words
        relevant_urls = (
            select(URL.id)
            .where(
                exists(
                    select(literal(1))
                    .where(
                        HTMLBagOfWords.type == bag_of_words_type.value,
                        HTMLBagOfWords.url_id == URL.id,
                    )
                )
            )
            .cte("relevant_urls")
        )
        relevant_url_id_col: ColumnElement[int] = relevant_urls.c.id

        # Get Total Number of documents with a Bag Of Words CTE (N)
        total_docs_query = (
            select(
                func.count(relevant_url_id_col).label("total_document_count")
            )
        )
        count_all_docs: int = await self.execute_scalar(
            session=session,
            query=total_docs_query
        )

        # CTE for top n terms
        top_n_terms = (
            select(HTMLBagOfWords.term_id)
            .where(HTMLBagOfWords.type == bag_of_words_type.value)
            .group_by(HTMLBagOfWords.term_id)
            .order_by(func.count(HTMLBagOfWords.url_id).desc())
            .limit(top_n_words)
            .cte("top_n_terms")
        )
        top_n_terms_id_col: ColumnElement[int] = top_n_terms.c.term_id



        # Cross join of all URLs with bag of words and top n terms
        url_term_cross_join = (
            select(
                relevant_url_id_col.label("url_id"),
                top_n_terms_id_col,
            )
            .select_from(relevant_urls)
            .outerjoin(
                top_n_terms,
                onclause=literal_column("1=1"),
                full=True)
            .cte("url_term_cross_join")
        )
        cross_url_id_col: ColumnElement[int] = url_term_cross_join.c.url_id
        cross_term_id_col: ColumnElement[int] = url_term_cross_join.c.term_id





        # Get CTE for each term and the number of URLs it appears in (n_t)
        count_docs_with_term_cte = (
            select(
                top_n_terms_id_col.label("term_id"),
                func.count(HTMLBagOfWords.url_id).label("term_count")
            )
            .join(
                HTMLBagOfWords,
                HTMLBagOfWords.term_id == top_n_terms_id_col
            )
            .where(HTMLBagOfWords.type == bag_of_words_type.value)
            .group_by(top_n_terms_id_col)
            .cte("term_counts")
        )
        count_docs_with_term_term_id_col: ColumnElement[int] = count_docs_with_term_cte.c.term_id
        count_docs_with_term_col: ColumnElement[int] = count_docs_with_term_cte.c.term_count

        # Get CTE for each document and the number of terms it contains (n_d)
        sum_func = func.sum(HTMLBagOfWords.count)
        count_all_terms_in_doc_cte = (
            select(
                relevant_url_id_col.label("url_id"),
                sum_func.label("doc_term_count")
            )
            .join(
                HTMLBagOfWords,
                HTMLBagOfWords.url_id == relevant_url_id_col
            )
            .where(HTMLBagOfWords.type == bag_of_words_type.value)
            .having(sum_func > min_doc_term_threshold)
            .group_by(relevant_url_id_col)
            .cte("doc_term_counts")
        )
        count_all_terms_in_doc_url_id_col: ColumnElement[int] = count_all_terms_in_doc_cte.c.url_id
        count_all_terms_in_doc_col: ColumnElement[int] = count_all_terms_in_doc_cte.c.doc_term_count

        count_term_in_doc_col: InstrumentedAttribute[int] = HTMLBagOfWords.count


        tf = count_term_in_doc_col / count_all_terms_in_doc_col
        idf = func.log(
            count_all_docs /
            func.coalesce(count_docs_with_term_col, 1)  # Account for nulls in join
        )
        tf_idf = cast(tf * idf, Float)

        final_subquery = (
            select(
                cross_url_id_col.label("url_id"),
                cross_term_id_col.label("term_id"),
                # Below used for debugging
                # func.coalesce(count_term_in_doc_col, 0).label("count_term_in_doc"),
                # count_all_terms_in_doc_col.label("count_all_terms_in_doc"),
                # literal(count_all_docs).label("count_all_documents"),
                # count_docs_with_term_col.label("count_docs_with_term"),
                # tf.label("tf"),
                # idf.label("idf"),
                tf_idf.label("tf_idf")
            )
            .outerjoin(
                HTMLBagOfWords,
                and_(
                    HTMLBagOfWords.url_id == cross_url_id_col,
                    HTMLBagOfWords.term_id == cross_term_id_col
                )
            )
            .join(
                count_docs_with_term_cte,
                count_docs_with_term_term_id_col == cross_term_id_col
            )
            .join(
                count_all_terms_in_doc_cte,
                count_all_terms_in_doc_url_id_col == cross_url_id_col
            )
            .where(
                HTMLBagOfWords.type == bag_of_words_type.value
            )
        ).subquery("tf_idf")

        tf_idf_term_id: ColumnElement[int] = final_subquery.c.term_id
        tf_idf_url_id: ColumnElement[int] = final_subquery.c.url_id
        tf_idf_value: ColumnElement[float] = final_subquery.c.tf_idf

        # Add annotations
        labels = BagOfWordsBaseLabels()

        final_query = (
            select(
                tf_idf_url_id.label(labels.url_id),
                tf_idf_term_id.label(labels.term_id),
                tf_idf_value.label(labels.tf_idf),
                URLAnnotations.relevant.label(labels.relevant),
                URLAnnotations.record_type_fine.label(labels.record_type_fine),
                URLAnnotations.record_type_coarse.label(labels.record_type_coarse)
            ).join(
                URLAnnotations,
                URLAnnotations.url_id == tf_idf_url_id,
            )
        )


        result = await self.execute_all(session=session, query=final_query)

        return LabeledDataFrame(
            df=pl.DataFrame(result),
            labels=labels
        )





