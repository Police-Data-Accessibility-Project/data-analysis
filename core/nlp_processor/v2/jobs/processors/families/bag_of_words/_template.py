from abc import ABC, abstractmethod
from typing import Type

from core.nlp_processor.v2.jobs.processors.job_processor_base import JobProcessorBase
from core.nlp_processor.v2.jobs.result.implementations import HTMLBagOfWordsJobResult
from core.nlp_processor.v2.jobs.result.job_result_base import JobResultBase


class ExtractHTMLBagOfWordsProcessorTemplate(JobProcessorBase, ABC):

    async def job_result_class(self) -> Type[JobResultBase]:
        return HTMLBagOfWordsJobResult

    @abstractmethod
    async def process(self) -> dict[str, int]:
        pass