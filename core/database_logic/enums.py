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

class HTMLContentMetricType(Enum):
    PROPER_NOUNS = "proper_nouns"
    LOCATION_NAMES = "location_names"
    PEOPLE_NAMES = "people_names"
    ORGANIZATION_NAMES = "organization_names"
    LEGAL_TERMS = "legal_terms"
    DATES_AND_TIMES = "dates_and_times"
    META_TAGS = "meta_tags"
    EMAILS = "emails"
    A_TAGS = "a_tags"
    P_TAGS = "p_tags"
    H_TAGS = "h_tags"
    H1_TAGS = "h1_tags"
    H2_TAGS = "h2_tags"
    H3_TAGS = "h3_tags"
    H4_TAGS = "h4_tags"
    H5_TAGS = "h5_tags"
    H6_TAGS = "h6_tags"
    UL_TAGS = "ul_tags"
    OL_TAGS = "ol_tags"
    LI_TAGS = "li_tags"
    DIV_TAGS = "div_tags"
    SPAN_TAGS = "span_tags"
    TABLE_TAGS = "table_tags"
    TR_TAGS = "tr_tags"
    TD_TAGS = "td_tags"
    TH_TAGS = "th_tags"
    FORM_TAGS = "form_tags"
    INPUT_TAGS = "input_tags"
    BUTTON_TAGS = "button_tags"
    IMG_TAGS = "img_tags"
    EXTERNAL_LINKS = "external_links"
    INTERNAL_LINKS = "internal_links"
    WORDS = "words"
    ALL_HTML_TAGS = "all_html_tags"
    SCRIPT_TAGS = "script_tags"

WORKING_CONTENT_METRIC_TYPES = [
    # HTMLContentMetricType.PROPER_NOUNS,
    # HTMLContentMetricType.LOCATION_NAMES,
    # HTMLContentMetricType.PEOPLE_NAMES,
    # HTMLContentMetricType.ORGANIZATION_NAMES,
    # HTMLContentMetricType.LEGAL_TERMS,
    # HTMLContentMetricType.DATES_AND_TIMES,
    # HTMLContentMetricType.EMAILS,
    # HTMLContentMetricType.META_TAGS,
    # HTMLContentMetricType.A_TAGS,
    # HTMLContentMetricType.P_TAGS,
    # HTMLContentMetricType.H_TAGS,
    # HTMLContentMetricType.H1_TAGS,
    # HTMLContentMetricType.H2_TAGS,
    # HTMLContentMetricType.H3_TAGS,
    # HTMLContentMetricType.H4_TAGS,
    # HTMLContentMetricType.H5_TAGS,
    # HTMLContentMetricType.H6_TAGS,
    # HTMLContentMetricType.UL_TAGS,
    # HTMLContentMetricType.OL_TAGS,
    # HTMLContentMetricType.LI_TAGS,
    # HTMLContentMetricType.DIV_TAGS,
    # HTMLContentMetricType.SPAN_TAGS,
    # HTMLContentMetricType.TABLE_TAGS,
    # HTMLContentMetricType.TR_TAGS,
    # HTMLContentMetricType.TD_TAGS,
    # HTMLContentMetricType.TH_TAGS,
    # HTMLContentMetricType.FORM_TAGS,
    # HTMLContentMetricType.INPUT_TAGS,
    # HTMLContentMetricType.BUTTON_TAGS,
    # HTMLContentMetricType.IMG_TAGS,
    # HTMLContentMetricType.EXTERNAL_LINKS,
    # HTMLContentMetricType.INTERNAL_LINKS,
    # HTMLContentMetricType.WORDS,
    # HTMLContentMetricType.ALL_HTML_TAGS,
    # HTMLContentMetricType.SCRIPT_TAGS,
]