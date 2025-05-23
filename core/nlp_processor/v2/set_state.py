from typing import List

from pydantic import BaseModel

from core.nlp_processor.dtos.batch_context import SetContext
from core.nlp_processor.v2.jobs.identifiers.job_identifier_base import JobIdentifierBase


class SetState(BaseModel):
    context: SetContext
    job_ids: List[JobIdentifierBase]