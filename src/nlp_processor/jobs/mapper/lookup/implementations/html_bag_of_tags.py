from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.core import HTMLBagOfTags, HTMLTag
from src.db.models.base import FamilyModel
from src.nlp_processor.jobs.mapper.lookup.base import LookupJobResultMapperBase
from src.nlp_processor.jobs.result.implementations.html_bag_of_tags.core import HTMLBagOfTagsJobResult


class HTMLBagOfTagsMapper(LookupJobResultMapperBase):

    async def map(
        self,
        url_id: int,
        result: HTMLBagOfTagsJobResult,
        session: AsyncSession
    ) -> list[FamilyModel]:
        all_tags = list(result.result.keys())
        if len(all_tags) == 0:
            return [HTMLBagOfTags(
                url_id=url_id,
                type=result.job_id.job_type.value,
                tag_id=None,
                count=0
            )]

        tag_map = await self.get_string_id_map(session, all_tags, HTMLTag)

        # Map tags to models
        models = []
        for tag in all_tags:
            model = HTMLBagOfTags(
                url_id=url_id,
                type=result.job_id.job_type.value,
                tag_id=tag_map[tag],
                count=result.result[tag]
            )
            models.append(model)

        return models
