from abc import ABC
from typing import Type

from core.nlp_processor.v2.jobs.processors.job_processor_base import JobProcessorBase
from core.nlp_processor.v2.jobs.result.implementations import HTMLContentMetricJobResult
from core.nlp_processor.v2.jobs.result.job_result_base import JobResultBase


class ExtractHTMLContentMetricProcessorTemplate(JobProcessorBase, ABC):

    async def job_result_class(self) -> Type[JobResultBase]:
        raise HTMLContentMetricJobResult

    async def process(self) -> int:
        pass