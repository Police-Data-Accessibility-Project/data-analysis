from abc import ABC, abstractmethod
from typing import Type, Optional

from core.nlp_processor.v2.jobs.processors.job_processor_base import JobProcessorBase
from core.nlp_processor.v2.jobs.result.implementations import URLComponentJobResult
from core.nlp_processor.v2.jobs.result.job_result_base import JobResultBase


class ExtractURLComponentProcessorTemplate(JobProcessorBase, ABC):

    async def job_result_class(self) -> Type[JobResultBase]:
        return URLComponentJobResult

    @abstractmethod
    async def process(self) -> Optional[str]:
        pass
