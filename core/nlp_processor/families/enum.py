from enum import Enum


class FamilyType(Enum):
    URL_COMPONENT = "url_component"
    HTML_METADATA = "html_metadata"
    HTML_CONTENT_METRIC = "html_content_metric"
    HTML_BAG_OF_WORDS = "html_bag_of_words"
    HTML_BAG_OF_TAGS = "html_bag_of_tags"
    HTML_TERM_TAG_COUNTS = "html_term_tag_counts"
