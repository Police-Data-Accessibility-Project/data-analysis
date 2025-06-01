from src.nlp_processor.jobs.identifiers.implementations import URLComponentJobIdentifier
from src.nlp_processor.jobs.processors.families.url_component.implementations import ExtractURLDomainProcessor, \
    ExtractURLSubdomainProcessor, ExtractURLSuffixProcessor, ExtractURLSchemeProcessor, ExtractURLPathProcessor, \
    ExtractURLFragmentProcessor, ExtractURLQueryParamsProcessor, ExtractURLFileFormatProcessor
from src.nlp_processor.jobs.enums import URLComponentJobType
from src.nlp_processor.jobs.registry.entry import JobRegistryEntry


def get_identifier(job_type: URLComponentJobType) -> URLComponentJobIdentifier:
    return URLComponentJobIdentifier(job_type=job_type)


URL_COMPONENT_JOBS = [
    JobRegistryEntry(
        identifier=get_identifier(URLComponentJobType.DOMAIN),
        processor=ExtractURLDomainProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(URLComponentJobType.SUBDOMAIN),
        processor=ExtractURLSubdomainProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(URLComponentJobType.SUFFIX),
        processor=ExtractURLSuffixProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(URLComponentJobType.SCHEME),
        processor=ExtractURLSchemeProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(URLComponentJobType.PATH),
        processor=ExtractURLPathProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(URLComponentJobType.FRAGMENT),
        processor=ExtractURLFragmentProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(URLComponentJobType.QUERY_PARAMS),
        processor=ExtractURLQueryParamsProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(URLComponentJobType.FILE_FORMAT),
        processor=ExtractURLFileFormatProcessor
    )
]