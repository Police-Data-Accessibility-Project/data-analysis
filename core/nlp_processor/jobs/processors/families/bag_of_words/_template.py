from abc import ABC, abstractmethod
from typing import Type

from core.nlp_processor.jobs.processors.base import JobProcessorBase
from core.nlp_processor.jobs.result.implementations import HTMLBagOfWordsJobResult
from core.nlp_processor.jobs.result.base import JobResultBase


class ExtractHTMLBagOfWordsProcessorTemplate(JobProcessorBase, ABC):

    async def job_result_class(self) -> Type[JobResultBase]:
        return HTMLBagOfWordsJobResult

    @abstractmethod
    async def process(self) -> dict[str, int]:
        pass