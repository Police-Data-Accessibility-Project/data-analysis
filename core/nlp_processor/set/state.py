from typing import List

from pydantic import BaseModel

from core.nlp_processor.set.context import SetContext
from core.nlp_processor.jobs.identifiers.base import JobIdentifierBase


class SetState(BaseModel):
    context: SetContext
    job_ids: List[JobIdentifierBase]