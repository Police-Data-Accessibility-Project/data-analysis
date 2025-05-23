from typing import Type

from pydantic import BaseModel

from core.nlp_processor.jobs.identifiers.base import JobIdentifierBase
from core.nlp_processor.jobs.processors.base import JobProcessorBase


class JobRegistryEntry(BaseModel):
    identifier: JobIdentifierBase
    processor: Type[JobProcessorBase]

