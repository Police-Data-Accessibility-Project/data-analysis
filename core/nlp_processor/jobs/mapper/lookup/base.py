from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.base import StringMapModel, FamilyModel
from core.nlp_processor.jobs.mapper.base import JobResultMapperBase
from core.nlp_processor.jobs.result.base import JobResultBase
from sqlalchemy.dialects.postgresql import insert as pg_insert

class LookupJobResultMapperBase(JobResultMapperBase, ABC):

    @abstractmethod
    async def map(
        self,
        result: JobResultBase,
        url_id: int,
        session: AsyncSession
    ) -> list[FamilyModel]:
        ...

    @staticmethod
    async def get_string_id_map(
        session: AsyncSession,
        strings: list[str],
        model: type[StringMapModel]
    ) -> dict[str, int]:
        existing_map = await LookupJobResultMapperBase.get_existing_string_id_map(
            session,
            strings,
            model
        )
        existing_strings = list(existing_map.keys())
        new_strings = list(set(strings) - set(existing_strings))
        if len(new_strings) == 0:
            return existing_map

        # Add any new strings and get their ids
        new_map = await LookupJobResultMapperBase.add_new_strings(
            session,
            new_strings,
            model
        )
        # Combine maps
        return {**existing_map, **new_map}


    @staticmethod
    async def get_existing_string_id_map(
        session: AsyncSession,
        strings: list[str],
        model: type[StringMapModel]
    ) -> dict[str, int]:
        stmt = (
            select(
                model.id,
                model.name,
            ).where(
                model.name.in_(strings)
            )
        )

        result = await session.execute(stmt)
        return {row.name: row.id for row in result}\

    @staticmethod
    async def add_new_strings(
        session: AsyncSession,
        strings: list[str],
        model: type[StringMapModel]
    ) -> dict[str, int]:
        if len(strings) == 0:
            return {}
        stmt = (
            pg_insert(model)
            .values([dict(name=strings) for strings in strings])
            .returning(model.id, model.name)
        )

        result = await session.execute(stmt)
        return {row.name: row.id for row in result}