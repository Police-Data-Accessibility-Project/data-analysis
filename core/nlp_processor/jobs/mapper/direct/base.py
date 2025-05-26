from abc import ABC, abstractmethod

from core.db.models.core import FamilyModel
from core.nlp_processor.jobs.result.base import JobResultBase

from core.nlp_processor.jobs.mapper.base import JobResultMapperBase
from core.nlp_processor.jobs.mapper.direct.protocol import DirectMapperProtocol


class DirectJobResultMapperBase(JobResultMapperBase, DirectMapperProtocol, ABC):

    @abstractmethod
    async def map(
        self,
        job_result: JobResultBase,
        url_id: int
    ) -> list[FamilyModel]:
        ...