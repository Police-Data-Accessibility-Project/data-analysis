from functools import wraps
from typing import Optional

from environs import Env
from sqlalchemy import select, outerjoin, not_, true, and_, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.compression_logic import decompress_html, compress_html
from core.database_logic.dtos.url_html_info import URLHTMLInfo
from core.database_logic.dtos.url_info import URLInfo
from core.database_logic.enums import ComponentType, ErrorType, HTMLMetadataType
from core.database_logic.models import URL, URLFullHTML, URLError, URLComponent, URLCompressedHTML
from core.database_logic.statement_composer import StatementComposer
from core.nlp_processor.dtos.batch_context import BatchContext
from core.nlp_processor.dtos.batch_jobs import BatchJobs
from core.nlp_processor.dtos.batch_state import BatchState
from core.nlp_processor.dtos.job_info.url_component_job_info import ComponentInfo, URLComponentJobInfo


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
        return [URLInfo(id=id, url=url) for id, url in raw_results]

        return [URLInfo(id=id, url=url) for id, url in raw_results]

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
        sc = StatementComposer

        query = (
            select(
                URL.id,
                URL.url,
                URLCompressedHTML.compressed_html,
                *[sc.url_component_type_exists(type_name) for type_name in ComponentType],
                *[sc.url_html_metadata_type_exists(type_name) for type_name in HTMLMetadataType],
            ).join(URLCompressedHTML)
            .outerjoin(URLComponent)
            .group_by(URL.id, URL.url, URLCompressedHTML.compressed_html)
            .having(
                not_(
                    and_(
                        *[
                            sc.url_component_type_exists(type_name) == True
                            for type_name in ComponentType
                        ],
                        *[
                            sc.url_html_metadata_type_exists(type_name) == True
                            for type_name in HTMLMetadataType
                        ]
                    )
                )
            ).limit(1)
        )

        execution_result = await session.execute(query)
        row = execution_result.mappings().one_or_none()

        if row is None:
            return None

        return BatchState(
            context=BatchContext(
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

    async def add_url_component(
        self,
        session: AsyncSession,
        url_id: int,
        component_info: ComponentInfo,
    ):
        url_component = URLComponent(
            url_id=url_id,
            type=component_info.type,
            value=component_info.value
        )
        session.add(url_component)

    @session_manager
    async def get_next_uncompressed_html(self, session: AsyncSession) -> URLHTMLInfo:
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
