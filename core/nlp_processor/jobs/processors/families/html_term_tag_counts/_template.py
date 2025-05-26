from abc import ABC, abstractmethod

from core.nlp_processor.jobs.processors.base import JobProcessorBase


class ExtractHTMLTermTagCountsProcessorTemplate(JobProcessorBase, ABC):

    @abstractmethod
    async def process(self) -> dict[str, dict[str, int]]:
        pass