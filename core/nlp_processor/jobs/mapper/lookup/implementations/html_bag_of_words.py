from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models.core import HTMLBagOfWords, HTMLTerm
from core.db.models.base import FamilyModel
from core.nlp_processor.jobs.mapper.lookup.base import LookupJobResultMapperBase
from core.nlp_processor.jobs.result.base import JobResultBase


class HTMLBagOfWordsMapper(LookupJobResultMapperBase):

    async def map(
        self,
        result: JobResultBase,
        url_id: int,
        session: AsyncSession
    ) -> list[FamilyModel]:
        all_terms = list(result.result.keys())
        if len(all_terms) == 0:
            return [HTMLBagOfWords(
                url_id=url_id,
                type=result.job_id.job_type.value,
                term_id=None,
                count=0
            )]

        word_map = await self.get_string_id_map(session, all_terms, HTMLTerm)

        # Map words to models
        models = []
        for word in all_terms:
            models.append(HTMLBagOfWords(
                url_id=url_id,
                type=result.job_id.job_type.value,
                term_id=word_map[word],
                count=result.result[word]
            ))

        return models
