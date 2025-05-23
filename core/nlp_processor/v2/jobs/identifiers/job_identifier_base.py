from pydantic import BaseModel

from core.nlp_processor.v2.families.enums import FamilyType
from core.nlp_processor.v2.jobs.enums import JobTypeEnumBase


class JobIdentifierBase(BaseModel):
    family: FamilyType
    job_type: JobTypeEnumBase

    def __hash__(self):
        return hash((self.family, self.job_type))
