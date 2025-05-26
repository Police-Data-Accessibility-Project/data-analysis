from typing import Protocol, runtime_checkable

from core.db.models.core import FamilyModel
from core.nlp_processor.jobs.result.base import JobResultBase

@runtime_checkable
class DirectMapperProtocol(Protocol):

    async def map(self, job_result: JobResultBase, url_id: int) -> list[FamilyModel]:
        ...

