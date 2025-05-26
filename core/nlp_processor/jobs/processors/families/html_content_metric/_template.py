from abc import ABC

from core.nlp_processor.jobs.processors.base import JobProcessorBase


class ExtractHTMLContentMetricProcessorTemplate(JobProcessorBase, ABC):

    async def process(self) -> int:
        pass