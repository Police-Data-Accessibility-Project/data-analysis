from enum import Enum


class FamilyType(Enum):
    URL_COMPONENT = "url_component"
    HTML_METADATA = "html_metadata"
    HTML_CONTENT_METRIC = "html_content_metric"
    HTML_BAG_OF_WORDS = "html_bag_of_words"
