from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.core import HTMLTag, HTMLTerm, HTMLTermTagCount
from core.db.models.base import FamilyModel
from core.nlp_processor.jobs.mapper.lookup.base import LookupJobResultMapperBase
from core.nlp_processor.jobs.result.implementations.html_term_tag_counts.core import HTMLTermTagCountJobResult
from core.nlp_processor.jobs.result.implementations.html_term_tag_counts.store import TermTagStore


class HTMLTermTagCountsMapper(LookupJobResultMapperBase):

    async def map(
        self,
        url_id: int,
        result: HTMLTermTagCountJobResult,
        session: AsyncSession
    ) -> list[FamilyModel]:
        store: TermTagStore = result.result

        all_terms = store.get_all_terms()
        all_tags = store.get_all_tags()

        tag_map = await self.get_string_id_map(session, all_tags, HTMLTag)
        term_map = await self.get_string_id_map(session, all_terms, HTMLTerm)

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
