from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.core import FamilyModel
from core.nlp_processor.jobs.result.base import JobResultBase
from core.nlp_processor.jobs.mapper.base import JobResultMapperBase
from core.nlp_processor.jobs.mapper.lookup.protocol import LookupMapperProtocol


class LookupJobResultMapperBase(JobResultMapperBase, LookupMapperProtocol, ABC):

    @abstractmethod
    async def map(
        self,
        result: JobResultBase,
        url_id: int,
        session: AsyncSession
    ) -> list[FamilyModel]:
        ...