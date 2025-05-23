from abc import ABC, abstractmethod
from typing import Type, Any, List

from pydantic import BaseModel

from core.database_logic.models import FamilyModel
from core.nlp_processor.v2.jobs.identifiers.job_identifier_base import JobIdentifierBase


class JobResultBase(BaseModel, ABC):
    job_id: JobIdentifierBase
    result: Any

    @abstractmethod
    def get_as_models(self, url_id: int) -> List[FamilyModel]:
        pass
