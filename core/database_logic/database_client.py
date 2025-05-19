from functools import wraps
from typing import Optional

from environs import Env
from sqlalchemy import select, outerjoin, not_, true, and_, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.database_logic.dtos.url_info import URLInfo
from core.database_logic.dtos.url_nlp_processing_info import URLNLPProcessingInfo
from core.database_logic.enums import ComponentType, ErrorType
from core.database_logic.models import URL, URLFullHTML, URLError, URLComponent
from core.database_logic.statement_composer import StatementComposer
from core.nlp_processor.dtos.url_html_processing_job_info import URLHTMLProcessingJobInfo
from core.nlp_processor.dtos.url_prereq_flags import URLPrereqFlags


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
        url_full_html = URLFullHTML(url_id=url_id, html=html)
        session.add(url_full_html)

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



    @session_manager
    async def get_urls_without_html(self, session: AsyncSession) -> list[URLInfo]:
        execution_result = await session.execute(
            select(
                URL.id,
                URL.url,
            )
            .outerjoin(URLFullHTML)
            .where(URLFullHTML.html.is_(None))
        )

        raw_results = execution_result.all()

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
    async def get_next_valid_url_for_nlp_preprocessing(self, session: AsyncSession) -> Optional[URLNLPProcessingInfo]:
        sc = StatementComposer

        query = select(
            URL.id,
            URL.url,
            URLFullHTML.html,
            *[sc.url_component_type_exists(type_name) for type_name in ComponentType],

        ).join(URLFullHTML).outerjoin(URLComponent).group_by(URL.id, URL.url, URLFullHTML.html).having(
            not_(and_(*[
                sc.url_component_type_exists(type_name) == True
                for type_name in ComponentType
            ]))
        ).limit(1)

        execution_result = await session.execute(query)
        row = execution_result.mappings().one_or_none()

        if row is None:
            return None

        return URLNLPProcessingInfo(
            job_info=URLHTMLProcessingJobInfo(
                url_info=URLInfo(
                    id=row["id"],
                    url=row["url"],
                ),
                html=row["html"],
            ),
            prereq_flags=URLPrereqFlags(
                url_component_scheme=row["has_scheme"],
                url_component_path=row["has_path"],
                url_component_domain=row["has_domain"],
                url_component_subdomain=row["has_subdomain"],
                url_component_fragment=row["has_fragment"],
                url_component_query_params=row["has_query_params"],
                url_component_file_format=row["has_file_format"],
                url_component_suffix=row["has_suffix"],
            )
        )

    @session_manager
    async def update_response_code(self, session: AsyncSession, url_id: int, response_code: int):
        await session.execute(
            update(URL)
            .where(URL.id == url_id)
            .values(response_code=response_code)
        )

    @session_manager
    async def add_url_component(
        self,
        session: AsyncSession,
        url_id: int,
        component_type: ComponentType,
        component_value: str
    ):
        url_component = URLComponent(
            url_id=url_id,
            type=component_type.value,
            value=component_value
        )
        session.add(url_component)