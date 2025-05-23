from abc import ABC
from typing import Type

from core.nlp_processor.jobs.processors.base import JobProcessorBase
from core.nlp_processor.jobs.result.implementations import HTMLContentMetricJobResult
from core.nlp_processor.jobs.result.base import JobResultBase


class ExtractHTMLContentMetricProcessorTemplate(JobProcessorBase, ABC):

    async def job_result_class(self) -> Type[JobResultBase]:
        raise HTMLContentMetricJobResult

    async def process(self) -> int:
        pass