"""
Job Processors are responsible for processing a single job for a single URL
Each processor operates on the URL and/or its HTML and extracts a single result
"""

from abc import ABC, abstractmethod
from typing import Type, Any

from bs4 import BeautifulSoup
from spacy.tokens.doc import Doc

from core.nlp_processor.dtos.batch_context import SetContext
from core.nlp_processor.v2.jobs.result.job_result_base import JobResultBase


class JobProcessorBase(ABC):

    def __init__(
        self,
        context: SetContext
    ):
        self.context = context

    @abstractmethod
    async def process(self) -> Any:
        pass

    @abstractmethod
    async def job_result_class(self) -> Type[JobResultBase]:
        pass

    @property
    def url(self) -> str:
        return self.context.url_info.url

    @property
    def url_id(self) -> int:
        return self.context.url_info.id

    @property
    def soup(self) -> BeautifulSoup:
        return self.context.soup

    @property
    def html(self) -> str:
        return self.context.html

    @property
    def spacy_doc(self) -> Doc:
        return self.context.spacy_doc
