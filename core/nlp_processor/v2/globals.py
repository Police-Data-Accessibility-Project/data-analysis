import spacy

from core.nlp_processor.v2.jobs.registry.core import JobRegistry
from core.nlp_processor.v2.jobs.registry.instances.bag_of_words import BAG_OF_WORDS_JOBS
from core.nlp_processor.v2.jobs.registry.instances.html_content_metric import HTML_CONTENT_METRIC_JOBS
from core.nlp_processor.v2.jobs.registry.instances.html_metadata import HTML_METADATA_JOBS
from core.nlp_processor.v2.jobs.registry.instances.url_component import URL_COMPONENT_JOBS

SPACY_MODEL = spacy.load('en_core_web_trf')  # Largest, slowest, most accurate model
# SPACY_MODEL = spacy.load('en_core_web_sm') # Smallest, fastest, least accurate model

JOB_REGISTRY = JobRegistry(
    [
        *BAG_OF_WORDS_JOBS,
        *HTML_CONTENT_METRIC_JOBS,
        *URL_COMPONENT_JOBS,
        *HTML_METADATA_JOBS
    ]
)