from typing import Type

from pydantic import BaseModel

from core.nlp_processor.v2.jobs.identifiers.job_identifier_base import JobIdentifierBase
from core.nlp_processor.v2.jobs.processors.job_processor_base import JobProcessorBase


class JobRegistryEntry(BaseModel):
    identifier: JobIdentifierBase
    processor: Type[JobProcessorBase]

