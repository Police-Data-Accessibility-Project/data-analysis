from enum import Enum


class JobTypeEnumBase(Enum):
    pass


class URLComponentJobType(JobTypeEnumBase):
    SCHEME = "scheme"
    DOMAIN = "domain"
    SUFFIX = "suffix"
    SUBDOMAIN = "subdomain"
    PATH = "path"
    FRAGMENT = "fragment"
    QUERY_PARAMS = "query_params"
    FILE_FORMAT = "file_format"


class HTMLMetadataJobType(JobTypeEnumBase):
    TITLE = "title"
    DESCRIPTION = "description"
    KEYWORDS = "keywords"
    AUTHOR = "author"

class HTMLContentMetricJobType(JobTypeEnumBase):
    PROPER_NOUNS = "proper_nouns"
    LOCATION_NAMES = "location_names"
    PEOPLE_NAMES = "people_names"
    ORGANIZATION_NAMES = "organization_names"
    LEGAL_TERMS = "legal_terms"
    DATES_AND_TIMES = "dates_and_times"
    EMAILS = "emails"
    EXTERNAL_LINKS = "external_links"
    INTERNAL_LINKS = "internal_links"
    WORDS = "words"
    CHARACTERS = "characters"

class HTMLBagOfWordsJobType(JobTypeEnumBase):
    ALL_WORDS = "all_words"
    LOCATIONS = "locations"
    PERSONS = "persons"
    COMMON_NOUNS = "common_nouns"
    PROPER_NOUNS = "proper_nouns"
    VERBS = "verbs"
    ADJECTIVES = "adjectives"
    ADVERBS = "adverbs"

class HTMLBagOfTagsJobType(JobTypeEnumBase):
    ALL_TAGS = "all_tags"

class HTMLTermTagCountsJobType(JobTypeEnumBase):
    ALL_WORDS = "all_words"