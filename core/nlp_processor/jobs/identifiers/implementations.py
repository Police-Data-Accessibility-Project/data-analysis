from core.nlp_processor.families.enum import FamilyType
from core.nlp_processor.jobs.identifiers.base import JobIdentifierBase
from core.nlp_processor.jobs.enums import HTMLBagOfWordsJobType, URLComponentJobType, HTMLMetadataJobType, \
    HTMLContentMetricJobType, HTMLTermTagCountsJobType, HTMLBagOfTagsJobType


class HTMLBagOfWordsJobIdentifier(JobIdentifierBase):
    family: FamilyType = FamilyType.HTML_BAG_OF_WORDS
    job_type: HTMLBagOfWordsJobType

class URLComponentJobIdentifier(JobIdentifierBase):
    family: FamilyType = FamilyType.URL_COMPONENT
    job_type: URLComponentJobType

class HTMLMetadataJobIdentifier(JobIdentifierBase):
    family: FamilyType = FamilyType.HTML_METADATA
    job_type: HTMLMetadataJobType

class HTMLContentMetricJobIdentifier(JobIdentifierBase):
    family: FamilyType = FamilyType.HTML_CONTENT_METRIC
    job_type: HTMLContentMetricJobType

class HTMLTermTagCountsJobIdentifier(JobIdentifierBase):
    family: FamilyType = FamilyType.HTML_TERM_TAG_COUNTS
    job_type: HTMLTermTagCountsJobType

class HTMLBagOfTagsJobIdentifier(JobIdentifierBase):
    family: FamilyType = FamilyType.HTML_BAG_OF_TAGS
    job_type: HTMLBagOfTagsJobType