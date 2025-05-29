from core.nlp_processor.jobs.registry.core import JobRegistry
from core.nlp_processor.jobs.registry.instances.html_bag_of_tags import HTML_BAG_OF_TAGS_JOBS
from core.nlp_processor.jobs.registry.instances.html_bag_of_words import HTML_BAG_OF_WORDS_JOBS
from core.nlp_processor.jobs.registry.instances.html_content_metric import HTML_CONTENT_METRIC_JOBS
from core.nlp_processor.jobs.registry.instances.html_metadata import HTML_METADATA_JOBS
from core.nlp_processor.jobs.registry.instances.html_term_tag_count import HTML_TERM_TAG_COUNT_JOBS
from core.nlp_processor.jobs.registry.instances.url_component import URL_COMPONENT_JOBS

JOB_REGISTRY = JobRegistry(
    [
        *HTML_BAG_OF_WORDS_JOBS,
        *HTML_BAG_OF_TAGS_JOBS,
        *HTML_CONTENT_METRIC_JOBS,
        *URL_COMPONENT_JOBS,
        *HTML_METADATA_JOBS,
        *HTML_TERM_TAG_COUNT_JOBS
    ]
)
