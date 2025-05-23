from typing import List

from core.db.models import FamilyModel, HTMLMetadata, URLComponent, HTMLContentMetric, HTMLBagOfWords
from core.nlp_processor.jobs.result.base import JobResultBase


class HTMLMetadataJobResult(JobResultBase):
    result: str

    def get_as_models(self, url_id: int) -> List[HTMLMetadata]:
        return [HTMLMetadata(
            url_id=url_id,
            type=self.job_id.job_type.value,
            value=self.result
        )]

class URLComponentJobResult(JobResultBase):
    result: str

    def get_as_models(self, url_id: int) -> List[URLComponent]:
        return [URLComponent(
            url_id=url_id,
            type=self.job_id.job_type.value,
            value=self.result
        )]

class HTMLContentMetricJobResult(JobResultBase):
    result: int

    def get_as_models(self, url_id: int) -> List[HTMLContentMetric]:
        return [HTMLContentMetric(
            url_id=url_id,
            type=self.job_id.job_type.value,
            value=self.result
        )]

class HTMLBagOfWordsJobResult(JobResultBase):
    result: dict[str, int]

    def get_as_models(self, url_id: int) -> List[FamilyModel]:
        if self.result == {}:
            return [HTMLBagOfWords(
                url_id=url_id,
                type=self.job_id.job_type.value,
                term=None,
                count=0
            )]

        models = []
        for word, count in self.result.items():
            models.append(HTMLBagOfWords(
                url_id=url_id,
                type=self.job_id.job_type.value,
                term=word,
                count=count
            ))

        return models