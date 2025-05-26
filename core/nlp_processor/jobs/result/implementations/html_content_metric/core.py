from core.nlp_processor.jobs.identifiers.implementations import HTMLContentMetricJobIdentifier
from core.nlp_processor.jobs.result.base import JobResultBase


class HTMLContentMetricJobResult(JobResultBase):
    job_id: HTMLContentMetricJobIdentifier
    result: int
