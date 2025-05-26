from core.db.models.core import FamilyModel, HTMLMetadata, URLComponent, HTMLContentMetric, HTMLBagOfWords
from core.nlp_processor.jobs.mapper.direct.base import DirectJobResultMapperBase
from core.nlp_processor.jobs.mapper.direct.factory import get_type_value_mapper
from core.nlp_processor.jobs.result.implementations.html_bag_of_words.core import HTMLBagOfWordsJobResult

HTMLMetadataMapper = get_type_value_mapper(HTMLMetadata)

URLComponentMapper = get_type_value_mapper(URLComponent)

HTMLContentMetricMapper = get_type_value_mapper(HTMLContentMetric)

class HTMLBagOfWordsMapper(DirectJobResultMapperBase):

    async def map(self, url_id: int, result: HTMLBagOfWordsJobResult) -> list[FamilyModel]:
        if result.result == {}:
            return [HTMLBagOfWords(
                url_id=url_id,
                type=result.job_id.job_type.value,
                term=None,
                count=0
            )]

        models = []
        for word, count in result.result.items():
            models.append(HTMLBagOfWords(
                url_id=url_id,
                type=result.job_id.job_type.value,
                term=word,
                count=count
            ))

        return models
