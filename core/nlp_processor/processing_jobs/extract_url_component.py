from abc import ABC, abstractmethod
from typing import Any, Optional

from tldextract import extract
from yarl import URL

from core.database_logic.enums import ComponentType
from core.nlp_processor.processing_jobs.url_html_processing_job_base import URLHTMLProcessingJobBase


class ExtractURLComponentBase(URLHTMLProcessingJobBase, ABC):

    async def download_additional_data(self):
        return None

    @property
    def process_name(self):
        return self.component_type.value

    @property
    @abstractmethod
    def component_type(self) -> ComponentType:
        pass

    @abstractmethod
    async def get_value_from_url(self) -> Optional[str]:
        pass

    async def process(self, data: Any):
        return await self.get_value_from_url()

class ExtractURLDomain(ExtractURLComponentBase):

    @property
    def component_type(self) -> ComponentType:
        return ComponentType.DOMAIN

    async def get_value_from_url(self):
        extract_result = extract(self.url)
        return extract_result.domain

class ExtractURLSuffix(ExtractURLComponentBase):

    @property
    def component_type(self) -> ComponentType:
        return ComponentType.SUFFIX

    async def get_value_from_url(self):
        extract_result = extract(self.url)
        return extract_result.suffix

class ExtractURLScheme(ExtractURLComponentBase):

    @property
    def component_type(self) -> ComponentType:
        return ComponentType.SCHEME

    async def get_value_from_url(self):
        url = URL(self.url)
        return url.scheme

class ExtractURLPath(ExtractURLComponentBase):

    @property
    def component_type(self) -> ComponentType:
        return ComponentType.PATH

    async def get_value_from_url(self):
        url = URL(self.url)
        return url.path

class ExtractURLSubdomain(ExtractURLComponentBase):

    @property
    def component_type(self) -> ComponentType:
        return ComponentType.SUBDOMAIN

    async def get_value_from_url(self):
        extract_result = extract(self.url)
        return extract_result.subdomain

class ExtractURLFragment(ExtractURLComponentBase):

    @property
    def component_type(self) -> ComponentType:
        return ComponentType.FRAGMENT

    async def get_value_from_url(self):
        url = URL(self.url)
        return url.fragment

class ExtractURLQueryParams(ExtractURLComponentBase):

    @property
    def component_type(self) -> ComponentType:
        return ComponentType.QUERY_PARAMS

    async def get_value_from_url(self) -> Optional[str]:
        url = URL(self.url)
        if not url.query:
            return None
        return str(url.query)

class ExtractURLFileFormat(ExtractURLComponentBase):

    @property
    def component_type(self) -> ComponentType:
        return ComponentType.FILE_FORMAT

    async def get_value_from_url(self) -> Optional[str]:
        url = URL(self.url)
        return url.suffix