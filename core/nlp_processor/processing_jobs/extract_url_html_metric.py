from abc import ABC, abstractmethod
from typing import Any

from core.database_logic.enums import HTMLContentMetricType
from core.nlp_processor.processing_jobs.url_html_processing_job_base import URLHTMLProcessingJobBase


class ExtractURLHTMLMetricBase(URLHTMLProcessingJobBase, ABC):

    async def download_additional_data(self):
        return None

    @property
    def process_name(self):
        return self.metric_type

    @property
    @abstractmethod
    def metric_type(self) -> HTMLContentMetricType:
        pass

    @abstractmethod
    def get_metric_value_from_html(self) -> int:
        pass

    async def process(self, data: Any):
        return

class ExtractURLHTMLMetricSingleTagBase(ExtractURLHTMLMetricBase, ABC):

    def get_metric_value_from_html(self) -> int:
        soup = self.context.soup
        tag_str = self.metric_type.value.replace("_tags", "")
        return len(soup.find_all(tag_str))


class ExtractURLHTMLMetricsATags(ExtractURLHTMLMetricSingleTagBase):
    @property
    def metric_type(self) -> HTMLContentMetricType:
        return HTMLContentMetricType.A_TAGS

class ExtractURLHTMLMetricsPTags(ExtractURLHTMLMetricSingleTagBase):
    @property
    def metric_type(self) -> HTMLContentMetricType:
        return HTMLContentMetricType.P_TAGS

class ExtractURLHTMLMetricsImgTags(ExtractURLHTMLMetricSingleTagBase):
    @property
    def metric_type(self) -> HTMLContentMetricType:
        return HTMLContentMetricType.IMG_TAGS