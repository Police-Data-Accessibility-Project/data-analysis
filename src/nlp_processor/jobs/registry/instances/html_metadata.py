from src.nlp_processor.jobs.identifiers.implementations import HTMLMetadataJobIdentifier
from src.nlp_processor.jobs.processors.families.html_metadata.implementations import \
    ExtractHTMLDescriptionMetadataProcessor, ExtractHTMLMetadataTitleProcessor, ExtractHTMLKeywordsMetadataProcessor, \
    ExtractHTMLAuthorMetadataProcessor
from src.nlp_processor.jobs.enums import HTMLMetadataJobType
from src.nlp_processor.jobs.registry.entry import JobRegistryEntry


def get_identifier(job_type: HTMLMetadataJobType) -> HTMLMetadataJobIdentifier:
    return HTMLMetadataJobIdentifier(job_type=job_type)

HTML_METADATA_JOBS = [
    JobRegistryEntry(
        identifier=get_identifier(HTMLMetadataJobType.DESCRIPTION),
        processor=ExtractHTMLDescriptionMetadataProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLMetadataJobType.TITLE),
        processor=ExtractHTMLMetadataTitleProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLMetadataJobType.KEYWORDS),
        processor=ExtractHTMLKeywordsMetadataProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLMetadataJobType.AUTHOR),
        processor=ExtractHTMLAuthorMetadataProcessor
    )
]