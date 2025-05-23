from abc import abstractmethod
from typing import Optional, Any

from bs4 import BeautifulSoup

from core.database_logic.enums import HTMLMetadataType
from core.nlp_processor.dtos.job_info.html_metadata_job_info import HTMLMetadataInfo
from core.nlp_processor.processing_jobs.url_html_processing_job_base import URLHTMLProcessingJobBase


class ExtractURLMetadataBase(URLHTMLProcessingJobBase):


    async def download_additional_data(self):
        return None

    @property
    def process_name(self):
        return self.metadata_type.value

    @property
    @abstractmethod
    def metadata_type(self) -> HTMLMetadataType:
        pass

    @abstractmethod
    async def get_metadata_value(self) -> Optional[str]:
        pass

    async def process(self, data: Any) -> HTMLMetadataInfo:
        value = await self.get_metadata_value()
        return HTMLMetadataInfo(
            type=self.metadata_type,
            value=value
        )

    @property
    def soup(self) -> BeautifulSoup:
        return self.context.soup

    def get_meta(self) -> Optional[str]:
        tag = self.soup.find(
            "meta",
            attrs={"name": self.metadata_type.value})
        return tag.get("content") if tag else None

class ExtractURLTitleMetadata(ExtractURLMetadataBase):
    @property
    def metadata_type(self):
        return HTMLMetadataType.TITLE

    async def get_metadata_value(self) -> Optional[str]:
        title = self.soup.title
        if not title:
            return None
        if not title.string:
            return None
        return title.string.strip()

class ExtractURLDescriptionMetadata(ExtractURLMetadataBase):
    @property
    def metadata_type(self):
        return HTMLMetadataType.DESCRIPTION

    async def get_metadata_value(self) -> Optional[str]:
        return self.get_meta()

class ExtractURLKeywordsMetadata(ExtractURLMetadataBase):
    @property
    def metadata_type(self):
        return HTMLMetadataType.KEYWORDS

    async def get_metadata_value(self) -> Optional[str]:
        return self.get_meta()

class ExtractURLAuthorMetadata(ExtractURLMetadataBase):
    @property
    def metadata_type(self):
        return HTMLMetadataType.AUTHOR

    async def get_metadata_value(self) -> Optional[str]:
        return self.get_meta()