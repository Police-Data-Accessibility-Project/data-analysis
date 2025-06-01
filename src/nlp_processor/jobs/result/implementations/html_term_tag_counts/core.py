from src.nlp_processor.jobs.identifiers.implementations import HTMLTermTagCountsJobIdentifier
from src.nlp_processor.jobs.result.base import JobResultBase
from src.nlp_processor.jobs.result.implementations.html_term_tag_counts.store import TermTagStore
from src.shared.bases.pydantic.arbitrary_base_model import ArbitraryBaseModel

class HTMLTermTagCountJobResult(ArbitraryBaseModel, JobResultBase):
    job_id: HTMLTermTagCountsJobIdentifier
    result: TermTagStore
