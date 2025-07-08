from functools import wraps
from typing import List, Dict, Any

import polars as pl
from environs import Env
from sqlalchemy import select, update, Select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.db.dtos.input.url_annotations import URLAnnotationsInput
from src.db.dtos.output.url import URLOutput
from src.db.enums import ErrorType
from src.db.models.core import URL, URLFullHTML, URLError, URLCompressedHTML, URLAnnotations
from src.db.queries.builder import QueryBuilderBase
from src.db.queries.ml_input_builder.bag_of_words_.builder import BagOfWordsMLInputQueryBuilder
from src.db.queries.ml_input_builder.raw.builder import RawMLInputQueryBuilder
from src.db.queries.nlp_processor.get_all_url_sets.builder import GetAllURLSetsQueryBuilder
from src.db.queries.nlp_processor.get_run_jobs.builder import GetRunJobsQueryBuilder
from src.nlp_processor.families.registry.instances import FAMILY_REGISTRY
from src.nlp_processor.jobs.enums import HTMLBagOfWordsJobType
from src.nlp_processor.jobs.identifiers.base import JobIdentifierBase
from src.nlp_processor.jobs.mapper.map import map_job_result_to_models
from src.nlp_processor.jobs.result.base import JobResultBase
from src.nlp_processor.set.state import SetState
from src.utils.compression import decompress_html, compress_html


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
    async def run_query_builder(self, session: AsyncSession, query_builder: QueryBuilderBase) -> Any:
        return await query_builder.build(session)

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

    async def get_run_jobs(
        self,
        job_ids: list[JobIdentifierBase]
    ) -> List[JobIdentifierBase]:
        """Get the set of jobs whose existence should be checked for all valid URLs in the database."""
        return await self.run_query_builder(
            query_builder=GetRunJobsQueryBuilder(job_ids)
        )


    async def get_all_url_sets(
        self,
        job_ids: List[JobIdentifierBase]
    ) -> List[SetState] | None:
        return await self.run_query_builder(
            query_builder=GetAllURLSetsQueryBuilder(job_ids)
        )

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

    async def get_bag_of_words_for_ml(
        self,
        bag_of_words_type: HTMLBagOfWordsJobType = HTMLBagOfWordsJobType.ALL_WORDS,
        top_n_words: int = 1000,
        min_doc_term_threshold: int = 100
    ) -> pl.DataFrame:

        return await self.run_query_builder(
            query_builder=BagOfWordsMLInputQueryBuilder(
                bag_of_words_type=bag_of_words_type,
                top_n_words=top_n_words,
                min_doc_term_threshold=min_doc_term_threshold
            )
        )

    async def get_raw_for_ml(
        self,
    ) -> pl.DataFrame:
        return await self.run_query_builder(
            query_builder=RawMLInputQueryBuilder()
        )