from core.nlp_processor.jobs.identifiers.implementations import HTMLBagOfTagsJobIdentifier
from core.nlp_processor.jobs.result.base import JobResultBase


class HTMLBagOfTagsJobResult(JobResultBase):
    job_id: HTMLBagOfTagsJobIdentifier
    result: dict[str, int]