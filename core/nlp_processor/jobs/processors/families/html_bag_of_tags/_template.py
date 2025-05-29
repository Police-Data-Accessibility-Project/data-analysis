from abc import ABC, abstractmethod

from core.nlp_processor.jobs.processors.base import JobProcessorBase


class ExtractHTMLBagOfTagsProcessorTemplate(JobProcessorBase, ABC):

    @abstractmethod
    async def process(self) -> dict[str, int]:
        pass