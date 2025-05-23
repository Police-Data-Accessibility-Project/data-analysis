from abc import ABC, abstractmethod
from typing import Any, Optional

from core.database_logic.database_client import DatabaseClient
from core.nlp_processor.dtos.batch_context import SetContext
from core.util import format_exception


class URLHTMLProcessingJobBase(ABC):

    def __init__(
        self,
        db_client: DatabaseClient,
        context: SetContext
    ):
        self.db_client = db_client
        self.context = context

    @property
    @abstractmethod
    def process_name(self):
        pass

    @abstractmethod
    async def download_additional_data(self) -> Any:
        pass

    @abstractmethod
    async def process(self, data: Any):
        pass

    async def run(self) -> Optional[Any]:
        try:
            data = await self.download_additional_data()
            return await self.process(data)
        except Exception as e:
            msg = format_exception(e)
            print(msg)
            await self.db_client.add_url_error(
                url_id=self.context.url_info.id,
                error=msg,
                error_type=self.process_name
            )
            return None

    @property
    def url(self):
        return self.context.url_info.url

    @property
    def url_id(self):
        return self.context.url_info.id