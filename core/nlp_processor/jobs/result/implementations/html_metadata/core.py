from core.nlp_processor.jobs.identifiers.implementations import HTMLMetadataJobIdentifier
from core.nlp_processor.jobs.result.base import JobResultBase


class HTMLMetadataJobResult(JobResultBase):
    job_id: HTMLMetadataJobIdentifier
    result: str
