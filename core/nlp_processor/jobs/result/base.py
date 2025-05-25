from abc import ABC, abstractmethod
from typing import Any, List

from pydantic import BaseModel

from core.db.models.core import FamilyModel
from core.nlp_processor.jobs.identifiers.base import JobIdentifierBase


class JobResultBase(BaseModel, ABC):
    job_id: JobIdentifierBase
    result: Any

    @abstractmethod
    def get_as_models(self, url_id: int) -> List[FamilyModel]:
        pass
