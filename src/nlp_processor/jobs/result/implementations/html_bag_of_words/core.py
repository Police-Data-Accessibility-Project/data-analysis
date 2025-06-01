from src.nlp_processor.jobs.identifiers.implementations import HTMLBagOfWordsJobIdentifier
from src.nlp_processor.jobs.result.base import JobResultBase


class HTMLBagOfWordsJobResult(JobResultBase):
    job_id: HTMLBagOfWordsJobIdentifier
    result: dict[str, int]
