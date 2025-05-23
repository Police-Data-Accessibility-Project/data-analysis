from abc import ABC
from typing import Optional

from core.database_logic.enums import HTMLMetadataType
from core.nlp_processor.v2.jobs.processors.families.html_metadata.factory import make_html_metadata_processor
from core.nlp_processor.v2.jobs.processors.families.html_metadata._template import ExtractHTMLMetadataProcessorTemplate

ExtractHTMLDescriptionMetadataProcessor = make_html_metadata_processor(
    HTMLMetadataType.DESCRIPTION
)
ExtractHTMLKeywordsMetadataProcessor = make_html_metadata_processor(
    HTMLMetadataType.KEYWORDS
)
ExtractHTMLAuthorMetadataProcessor = make_html_metadata_processor(
    HTMLMetadataType.AUTHOR
)


class ExtractHTMLMetadataTitleProcessor(ExtractHTMLMetadataProcessorTemplate, ABC):

    async def process(self) -> Optional[str]:
        title = self.soup.title
        if not title:
            return None
        if not title.string:
            return None
        return title.string.strip()
