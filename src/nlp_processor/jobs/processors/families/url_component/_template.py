from abc import ABC, abstractmethod
from typing import Optional

from src.nlp_processor.jobs.processors.base import JobProcessorBase


class ExtractURLComponentProcessorTemplate(JobProcessorBase, ABC):

    @abstractmethod
    async def process(self) -> Optional[str]:
        pass
