from pydantic import BaseModel

from core.database_logic.models import FamilyModel
from core.nlp_processor.v2.families.enums import FamilyType
from core.nlp_processor.v2.jobs.result.job_result_base import JobResultBase


class FamilyRegistryEntry(BaseModel):
    family: FamilyType
    model: type[FamilyModel]
    job_result_class: type[JobResultBase]