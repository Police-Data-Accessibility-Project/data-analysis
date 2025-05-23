from abc import ABC
from typing import Optional

from core.nlp_processor.jobs.enums import HTMLMetadataJobType
from core.nlp_processor.jobs.processors.families.html_metadata._template import ExtractHTMLMetadataProcessorTemplate
from core.nlp_processor.jobs.processors.families.html_metadata.factory import make_html_metadata_processor

ExtractHTMLDescriptionMetadataProcessor = make_html_metadata_processor(
    HTMLMetadataJobType.DESCRIPTION
)
ExtractHTMLKeywordsMetadataProcessor = make_html_metadata_processor(
    HTMLMetadataJobType.KEYWORDS
)
ExtractHTMLAuthorMetadataProcessor = make_html_metadata_processor(
    HTMLMetadataJobType.AUTHOR
)


class ExtractHTMLMetadataTitleProcessor(ExtractHTMLMetadataProcessorTemplate, ABC):

    async def process(self) -> Optional[str]:
        title = self.soup.title
        if not title:
            return None
        if not title.string:
            return None
        return title.string.strip()
