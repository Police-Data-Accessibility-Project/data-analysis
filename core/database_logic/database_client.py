from functools import wraps
from typing import Optional, List, Type

from environs import Env
from sqlalchemy import select, not_, and_, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.compression_logic import decompress_html, compress_html
from core.database_logic.dtos.url_html_info import URLHTMLInfo
from core.database_logic.dtos.url_info import URLInfo
from core.database_logic.enums import ComponentType, ErrorType, HTMLMetadataType, WORKING_CONTENT_METRIC_TYPES
from core.database_logic.models import URL, URLFullHTML, URLError, URLComponent, URLCompressedHTML, HTMLMetadata, \
    HTMLContentMetric
from core.database_logic.statement_composer import ExistsQueryCreator
from core.nlp_processor.dtos.batch_context import SetContext
from core.nlp_processor.dtos.batch_jobs import BatchJobs
from core.nlp_processor.dtos.batch_state import BatchState
from core.nlp_processor.dtos.job_info.html_metadata_job_info import HTMLMetadataJobInfo, HTMLMetadataInfo
from core.nlp_processor.dtos.job_info.url_component_job_info import ComponentInfo, URLComponentJobInfo
from core.nlp_processor.v2.check_query_builder import CheckQueryBuilder
from core.nlp_processor.v2.jobs.identifiers.job_identifier_base import JobIdentifierBase
from core.nlp_processor.v2.jobs.result.job_result_base import JobResultBase
from core.nlp_processor.v2.set_state import SetState


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
    async def get_urls_without_response_codes(self, session: AsyncSession) -> list[URLInfo]:
        execution_result = await session.execute(
            select(
                URL.id,
                URL.url,
            )
            .where(URL.response_code.is_(None))
        )
        raw_results = execution_result.all()
        return [URLInfo(id=id_, url=url) for id_, url in raw_results]

        return [URLInfo(id=id_, url=url) for id_, url in raw_results]

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
    async def get_next_valid_url_batch_for_nlp_preprocessing(self, session: AsyncSession) -> Optional[BatchState]:
        component_type_exists_creator = ExistsQueryCreator(
            attribute=URLComponent.type, valid_enums=ComponentType
        )
        html_metadata_type_exists_creator = ExistsQueryCreator(
            attribute=HTMLMetadata.type, valid_enums=HTMLMetadataType
        )
        html_content_metric_type_exists_creator = ExistsQueryCreator(
            attribute=HTMLContentMetric.type, valid_enums=WORKING_CONTENT_METRIC_TYPES
        )

        query = (
            select(
                URL.id,
                URL.url,
                URLCompressedHTML.compressed_html,
                *component_type_exists_creator.select(),
                *html_metadata_type_exists_creator.select(),
                *html_content_metric_type_exists_creator.select(),
            ).join(URLCompressedHTML)
            .outerjoin(URLComponent)
            .outerjoin(HTMLMetadata)
            .group_by(URL.id, URL.url, URLCompressedHTML.compressed_html)
            .having(
                not_(
                    and_(
                        *component_type_exists_creator.where(),
                        *html_metadata_type_exists_creator.where(),
                        *html_content_metric_type_exists_creator.where(),
                    )
                )
            ).limit(1)
        )

        execution_result = await session.execute(query)
        row = execution_result.mappings().one_or_none()

        if row is None:
            return None

        return BatchState(
            context=SetContext(
                url_info=URLInfo(
                    id=row["id"],
                    url=row["url"],
                ),
                html=decompress_html(row["compressed_html"]),
            ),
            jobs=BatchJobs.initialize_with_processed_flags(
                url_component_scheme=row["has_scheme"],
                url_component_path=row["has_path"],
                url_component_domain=row["has_domain"],
                url_component_subdomain=row["has_subdomain"],
                url_component_fragment=row["has_fragment"],
                url_component_query_params=row["has_query_params"],
                url_component_file_format=row["has_file_format"],
                url_component_suffix=row["has_suffix"],
                html_metadata_title=row["has_title"],
                html_metadata_description=row["has_description"],
                html_metadata_keywords=row["has_keywords"],
                html_metadata_author=row["has_author"],
            )
        )

    @session_manager
    async def update_response_code(self, session: AsyncSession, url_id: int, response_code: int):
        await session.execute(
            update(URL)
            .where(URL.id == url_id)
            .values(response_code=response_code)
        )

    @staticmethod
    async def add_url_component(
        session: AsyncSession,
        url_id: int,
        component_info: ComponentInfo,
    ):
        url_component = URLComponent(
            url_id=url_id,
            type=component_info.type.value,
            value=component_info.value
        )
        session.add(url_component)

    @session_manager
    async def get_next_uncompressed_html(self, session: AsyncSession) -> Optional[URLHTMLInfo]:
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

        return URLHTMLInfo(
            url_id=row["id"],
            html=row["html"],
        )

    @session_manager
    async def add_compressed_html(self, session: AsyncSession, url_id: int, compressed_html: bytes):
        url_compressed_html = URLCompressedHTML(url_id=url_id, compressed_html=compressed_html)
        session.add(url_compressed_html)

    @session_manager
    async def upload_batch_jobs(
            self,
            session: AsyncSession,
            url_id: int,
            jobs: BatchJobs
    ):
        # Process components
        components: list[URLComponentJobInfo] = [
            jobs.url_component_scheme,
            jobs.url_component_path,
            jobs.url_component_domain,
            jobs.url_component_subdomain,
            jobs.url_component_fragment,
            jobs.url_component_query_params,
            jobs.url_component_file_format,
            jobs.url_component_suffix,
        ]
        for job_info in components:
            if job_info.processed:
                continue
            await self.add_url_component(
                session=session,
                url_id=url_id,
                component_info=job_info.value
            )

        # Process HTML metadata
        metadata: list[HTMLMetadataJobInfo] = [
            jobs.html_metadata_title,
            jobs.html_metadata_description,
            jobs.html_metadata_keywords,
            jobs.html_metadata_author,
        ]
        for job_info in metadata:
            if job_info.processed:
                continue
            await self.add_html_metadata(
                session=session,
                url_id=url_id,
                metadata_info=job_info.value
            )

    @staticmethod
    async def add_html_metadata(
        session: AsyncSession,
        url_id: int,
        metadata_info: HTMLMetadataInfo
    ):
        html_metadata = HTMLMetadata(
            url_id=url_id,
            type=metadata_info.type.value,
            value=metadata_info.value
        )
        session.add(html_metadata)


    @session_manager
    async def get_run_jobs(
        self,
        session: AsyncSession,
        job_ids: List[Type[JobIdentifierBase]]
    ) -> List[Type[JobIdentifierBase]]:
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
        job_ids: List[Type[JobIdentifierBase]]
    ) -> Optional[SetState]:
        """
        Get the set of jobs for this URL, aka all jobs which have NOT yet been performed on this URL
        :param session:
        :param job_ids:
        :return:
        """
        builder = CheckQueryBuilder(job_ids)
        select_subqueries = builder.get_flag_select_subqueries()
        where_subqueries = [subquery == False for subquery in select_subqueries if subquery is not None]

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
            not_(
                and_(
                    *where_subqueries
                )
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
                url_info=URLInfo(
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