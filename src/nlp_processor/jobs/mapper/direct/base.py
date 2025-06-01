from abc import ABC, abstractmethod

from src.db.models.base import FamilyModel
from src.nlp_processor.jobs.mapper.base import JobResultMapperBase
from src.nlp_processor.jobs.result.base import JobResultBase


class DirectJobResultMapperBase(JobResultMapperBase, ABC):

    @abstractmethod
    async def map(
        self,
        job_result: JobResultBase,
        url_id: int
    ) -> list[FamilyModel]:
        ...