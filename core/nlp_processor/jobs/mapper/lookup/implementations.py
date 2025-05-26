from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.core import FamilyModel, HTMLTermTagCount, HTMLTag, StringMapModel, HTMLTerm
from core.nlp_processor.jobs.mapper.lookup.base import LookupJobResultMapperBase
from core.nlp_processor.jobs.result.implementations.html_term_tag_counts.core import HTMLTermTagCountJobResult
from core.nlp_processor.jobs.result.implementations.html_term_tag_counts.store import TermTagStore


class HTMLTermTagCountsMapper(LookupJobResultMapperBase):

    # TODO: This can be generalized to a factory function once we add similar mappers
    @staticmethod
    async def get_string_id_map(session: AsyncSession, strings: list[str], model: type[StringMapModel]) -> dict[str, int]:
        stmt = (
            select(
                model.id,
                model.name,
            ).where(
                model.name.in_(strings)
            )
        )

        result = await session.execute(stmt)
        return {row.name: row.id for row in result}


    async def get_existing_tag_id_map(self, session: AsyncSession, tags: list[str]) -> dict[str, int]:
        return await self.get_string_id_map(session, tags, HTMLTag)

    async def get_existing_term_id_map(self, session: AsyncSession, terms: list[str]) -> dict[str, int]:
        return await self.get_string_id_map(session, terms, HTMLTerm)

    @staticmethod
    async def add_new_strings(session: AsyncSession, strings: list[str], model: type[StringMapModel]) -> dict[str, int]:
        if len(strings) == 0:
            return {}
        stmt = (
            pg_insert(model)
            .values([dict(name=strings) for strings in strings])
            .returning(model.id, model.name)
        )

        result = await session.execute(stmt)
        return {row.name: row.id for row in result}

    async def add_new_tags(self, session: AsyncSession, tags: list[str]) -> dict[str, int]:
        return await self.add_new_strings(session, tags, HTMLTag)

    async def add_new_terms(self, session: AsyncSession, terms: list[str]) -> dict[str, int]:
        return await self.add_new_strings(session, terms, HTMLTerm)

    async def map(
        self,
        url_id: int,
        result: HTMLTermTagCountJobResult,
        session: AsyncSession
    ) -> list[FamilyModel]:
        store: TermTagStore = result.result

        # TODO: This logic can be generalized considerably once we add similar mappers

        all_terms = store.get_all_terms()
        all_tags = store.get_all_tags()

        # First, get all existing tags and terms
        existing_tag_map = await self.get_existing_tag_id_map(session, all_tags)
        existing_term_map = await self.get_existing_term_id_map(session, all_terms)

        # Identify new tags and terms
        new_tags = list(set(store.get_all_tags()) - set(existing_tag_map.keys()))
        new_terms = list(set(all_terms) - set(existing_term_map.keys()))

        # For tags and terms that do not exist, add them to the database and return their ids
        new_tag_map = await self.add_new_tags(session, new_tags)
        new_term_map = await self.add_new_terms(session, new_terms)

        # Combine maps of existing tags and terms with maps of new tags and terms
        tag_map = {**existing_tag_map, **new_tag_map}
        term_map = {**existing_term_map, **new_term_map}

        # Map tags and terms to models
        models = []
        for term in all_terms:
            for tag in store.get_tags_for_term(term):
                model = HTMLTermTagCount(
                    url_id=url_id,
                    type=result.job_id.job_type.value,
                    tag_id=tag_map[tag],
                    term_id=term_map[term],
                    count=store.get(term, tag)
                )
                models.append(model)

        return models


