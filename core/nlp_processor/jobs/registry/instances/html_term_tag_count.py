from core.nlp_processor.jobs.enums import HTMLTermTagCountsJobType
from core.nlp_processor.jobs.identifiers.implementations import HTMLTermTagCountsJobIdentifier
from core.nlp_processor.jobs.processors.families.html_term_tag_counts.implementations import HTMLTermTagCountsProcessor
from core.nlp_processor.jobs.registry.entry import JobRegistryEntry

HTML_TERM_TAG_COUNT_JOBS = [
    JobRegistryEntry(
        identifier=HTMLTermTagCountsJobIdentifier(job_type=HTMLTermTagCountsJobType.ALL_WORDS),
        processor=HTMLTermTagCountsProcessor
    ),
]