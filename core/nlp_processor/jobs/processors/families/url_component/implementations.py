from tldextract import extract
from yarl import URL

from core.nlp_processor.jobs.processors.families.url_component.factory import make_url_component_processor
from core.nlp_processor.jobs.enums import URLComponentJobType

UCT = URLComponentJobType  # Alias to reduce verbosity below

ExtractURLDomainProcessor = make_url_component_processor(
    UCT.DOMAIN, lambda url: extract(url).domain
)

ExtractURLSuffixProcessor = make_url_component_processor(
    UCT.SUFFIX, lambda url: extract(url).suffix
)

ExtractURLSchemeProcessor = make_url_component_processor(
    UCT.SCHEME, lambda url: URL(url).scheme
)

ExtractURLPathProcessor = make_url_component_processor(
    UCT.PATH, lambda url: URL(url).path
)

ExtractURLSubdomainProcessor = make_url_component_processor(
    UCT.SUBDOMAIN, lambda url: extract(url).subdomain
)

ExtractURLFragmentProcessor = make_url_component_processor(
    UCT.FRAGMENT, lambda url: URL(url).fragment
)

ExtractURLQueryParamsProcessor = make_url_component_processor(
    UCT.QUERY_PARAMS,
    lambda url: str(URL(url).query) if URL(url).query else None
)

ExtractURLFileFormatProcessor = make_url_component_processor(
    UCT.FILE_FORMAT, lambda url: URL(url).suffix
)