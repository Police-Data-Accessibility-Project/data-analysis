from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.base import FamilyModel
from src.nlp_processor.jobs.mapper.base import JobResultMapperBase
from src.nlp_processor.jobs.mapper.direct.base import DirectJobResultMapperBase
from src.nlp_processor.jobs.mapper.lookup.base import LookupJobResultMapperBase
from src.nlp_processor.jobs.result.base import JobResultBase


async def map_job_result_to_models(
    job_result: JobResultBase,
    mapper_class: type[JobResultMapperBase],
    url_id: int,
    session: AsyncSession
) -> list[FamilyModel]:

    mapper: JobResultMapperBase = mapper_class()
    if isinstance(mapper, LookupJobResultMapperBase):
        mapper = cast(LookupJobResultMapperBase, mapper)
        return await mapper.map(
            result=job_result,
            url_id=url_id,
            session=session
        )
    mapper = cast(DirectJobResultMapperBase, mapper)
    return await mapper.map(
        result=job_result,
        url_id=url_id
    )