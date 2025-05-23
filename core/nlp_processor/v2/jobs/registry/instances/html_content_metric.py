
from core.nlp_processor.v2.jobs.identifiers.implementations import HTMLContentMetricJobIdentifier
from core.nlp_processor.v2.jobs.processors.families.html_content_metric.implementations import \
    ExtractHTMLContentMetricsInternalLinkProcessor, ExtractHTMLContentMetricsExternalLinkProcessor
from core.nlp_processor.v2.jobs.enums import HTMLContentMetricJobType
from core.nlp_processor.v2.jobs.registry.entry import JobRegistryEntry


def get_identifier(job_type: HTMLContentMetricJobType) -> HTMLContentMetricJobIdentifier:
    return HTMLContentMetricJobIdentifier(job_type=job_type)


HTML_CONTENT_METRIC_JOBS = [
    JobRegistryEntry(
        identifier=get_identifier(HTMLContentMetricJobType.INTERNAL_LINKS),
        processor=ExtractHTMLContentMetricsInternalLinkProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLContentMetricJobType.EXTERNAL_LINKS),
        processor=ExtractHTMLContentMetricsExternalLinkProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLContentMetricJobType.EMAILS),
        processor=ExtractHTMLContentMetricsExternalLinkProcessor
    )
]