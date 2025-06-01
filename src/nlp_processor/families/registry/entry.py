from pydantic import BaseModel

from src.db.models.base import FamilyModel
from src.nlp_processor.families.enum import FamilyType
from src.nlp_processor.jobs.mapper.base import JobResultMapperBase
from src.nlp_processor.jobs.result.base import JobResultBase


class FamilyRegistryEntry(BaseModel):
    family: FamilyType
    model: type[FamilyModel]
    job_result_class: type[JobResultBase]
    mapper_class: type[JobResultMapperBase]