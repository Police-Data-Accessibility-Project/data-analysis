from abc import ABC, abstractmethod
from typing import Type, Optional

from core.nlp_processor.v2.jobs.processors.job_processor_base import JobProcessorBase
from core.nlp_processor.v2.jobs.result.implementations import HTMLMetadataJobResult
from core.nlp_processor.v2.jobs.result.job_result_base import JobResultBase


class ExtractHTMLMetadataProcessorTemplate(JobProcessorBase, ABC):

    async def job_result_class(self) -> Type[JobResultBase]:
        return HTMLMetadataJobResult

    @abstractmethod
    async def process(self) -> Optional[str]:
        pass
