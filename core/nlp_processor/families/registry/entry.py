from pydantic import BaseModel

from core.db.models.core import FamilyModel
from core.nlp_processor.families.enum import FamilyType
from core.nlp_processor.jobs.result.base import JobResultBase


class FamilyRegistryEntry(BaseModel):
    family: FamilyType
    model: type[FamilyModel]
    job_result_class: type[JobResultBase]