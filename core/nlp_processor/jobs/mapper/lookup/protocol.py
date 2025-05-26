from typing import Protocol, runtime_checkable

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.core import FamilyModel
from core.nlp_processor.jobs.result.base import JobResultBase

@runtime_checkable
class LookupMapperProtocol(Protocol):

    async def map(
        self,
        result: JobResultBase,
        url_id: int,
        session: AsyncSession
    ) -> list[FamilyModel]:
        ...