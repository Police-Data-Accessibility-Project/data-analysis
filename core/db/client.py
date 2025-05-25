from functools import wraps
from typing import Optional, List, Dict

from environs import Env
from sqlalchemy import select, update, or_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.db.dtos.input.url_annotations import URLAnnotationsInput
from core.utils.compression import decompress_html, compress_html
from core.db.dtos.input.url_html import URLHTMLInput
from core.db.dtos.output.url import URLOutput
from core.db.enums import ErrorType
from core.db.models.core import URL, URLFullHTML, URLError, URLCompressedHTML, URLAnnotations
from core.nlp_processor.check_query_builder import CheckQueryBuilder
from core.nlp_processor.jobs.identifiers.base import JobIdentifierBase
from core.nlp_processor.jobs.result.base import JobResultBase
from core.nlp_processor.set.context import SetContext
from core.nlp_processor.set.state import SetState


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
            async with self.session_maker() as session:
                async with session.begin():
                    try:
                        result = await method(self, session, *args, **kwargs)
                        return result
                    except Exception as e:
                        await session.rollback()
                        raise e

        return wrapper

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

    @session_manager
    async def get_urls_without_response_codes(self, session: AsyncSession) -> list[URLOutput]:
        execution_result = await session.execute(
            select(
                URL.id,
                URL.url,
            )
            .where(URL.response_code.is_(None))
        )
        raw_results = execution_result.all()
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
    async def get_next_uncompressed_html(self, session: AsyncSession) -> Optional[URLHTMLInput]:
        execution_result = await session.execute(
            select(
                URL.id,
                URLFullHTML.html,
            )
            .join(URLFullHTML)
            .outerjoin(URLCompressedHTML)
            .where(URLFullHTML.html != None)
            .where(URLCompressedHTML.id.is_(None))
            .limit(1)
        )
        row = execution_result.mappings().one_or_none()

        if row is None:
            return None

        return URLHTMLInput(
            url_id=row["id"],
            html=row["html"],
        )

    @session_manager
    async def add_compressed_html(self, session: AsyncSession, url_id: int, compressed_html: bytes):
        url_compressed_html = URLCompressedHTML(url_id=url_id, compressed_html=compressed_html)
        session.add(url_compressed_html)

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
    async def get_next_url_set(
        self,
        session: AsyncSession,
        job_ids: List[JobIdentifierBase]
    ) -> Optional[SetState]:
        """
        Get the set of jobs for this URL, aka all jobs which have NOT yet been performed on this URL
        :param session:
        :param job_ids:
        :return:
        """
        if len(job_ids) == 0:
            return None

        builder = CheckQueryBuilder(job_ids)
        select_subqueries = builder.get_flag_select_subqueries()

        query = select(
            URL.id,
            URL.url,
            URLCompressedHTML.compressed_html,
            *select_subqueries
        ).join(
            URLCompressedHTML
        )

        # Outer join for every family with jobs present
        query = builder.add_family_outer_joins(query)

        # Finalize Query
        query = query.group_by(
            URL.id,
            URL.url,
            URLCompressedHTML.compressed_html
        ).having(
            or_(
                *select_subqueries
            )
        ).limit(1)

        execution_result = await session.execute(query)
        row = execution_result.mappings().one_or_none()

        if row is None:
            return None

        set_jobs = []
        for label in builder.get_all_labels():
            url_missing_job = row[label]
            if url_missing_job:
                job_id = builder.get_job_id_from_label(label)
                set_jobs.append(job_id)

        return SetState(
            context=SetContext(
                url_info=URLOutput(
                    id=row["id"],
                    url=row["url"],
                ),
                html=decompress_html(row["compressed_html"]),
            ),
            job_ids=set_jobs
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
            models = job_result.get_as_models(url_id)
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