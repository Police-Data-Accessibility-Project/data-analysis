from pydantic import ConfigDict

from core.nlp_processor.jobs.identifiers.implementations import HTMLTermTagCountsJobIdentifier
from core.nlp_processor.jobs.result.base import JobResultBase
from core.nlp_processor.jobs.result.implementations.html_term_tag_counts.store import TermTagStore


class HTMLTermTagCountJobResult(JobResultBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    job_id: HTMLTermTagCountsJobIdentifier
    result: TermTagStore
