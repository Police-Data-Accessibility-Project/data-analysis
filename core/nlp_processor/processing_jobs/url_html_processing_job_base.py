from abc import ABC, abstractmethod
from typing import Any

from core.database_logic.database_client import DatabaseClient
from core.nlp_processor.dtos.url_html_processing_job_info import URLHTMLProcessingJobInfo
from core.util import format_exception


class URLHTMLProcessingJobBase(ABC):

    def __init__(
        self,
        db_client: DatabaseClient,
        job_info: URLHTMLProcessingJobInfo
    ):
        self.db_client = db_client
        self.job_info = job_info

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

    @abstractmethod
    async def upload_results(self, processed_data: Any):
        pass

    async def run(self):
        try:
            data = await self.download_additional_data()
            processed_data = await self.process(data)
            await self.upload_results(processed_data)
        except Exception as e:
            msg = format_exception(e)
            await self.db_client.add_url_error(
                url_id=self.job_info.url_info.id,
                error=msg,
                error_type=self.process_name
            )

    @property
    def url(self):
        return self.job_info.url_info.url

    @property
    def url_id(self):
        return self.job_info.url_info.id