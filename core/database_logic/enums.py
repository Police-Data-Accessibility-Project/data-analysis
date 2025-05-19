from enum import Enum


class ComponentType(Enum):
    SCHEME = "scheme"
    DOMAIN = "domain"
    SUFFIX = "suffix"
    SUBDOMAIN = "subdomain"
    PATH = "path"
    FRAGMENT = "fragment"
    QUERY_PARAMS = "query_params"
    FILE_FORMAT = "file_format"

class ErrorType(Enum):
    SCRAPE = "scrape"
    PARSE = "parse"

class HTMLMetadataType(Enum):
    TITLE = "title"
    DESCRIPTION = "description"
    KEYWORDS = "keywords"
    AUTHOR = "author"