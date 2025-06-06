from src.nlp_processor.jobs.identifiers.implementations import URLComponentJobIdentifier
from src.nlp_processor.jobs.result.base import JobResultBase


class URLComponentJobResult(JobResultBase):
    job_id: URLComponentJobIdentifier
    result: str
