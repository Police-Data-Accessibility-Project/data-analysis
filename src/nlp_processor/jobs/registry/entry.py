from typing import Type

from pydantic import BaseModel

from src.nlp_processor.jobs.identifiers.base import JobIdentifierBase
from src.nlp_processor.jobs.processors.base import JobProcessorBase


class JobRegistryEntry(BaseModel):
    identifier: JobIdentifierBase
    processor: Type[JobProcessorBase]

