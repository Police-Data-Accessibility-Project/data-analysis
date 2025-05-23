from typing import Optional

from core.database_logic.enums import HTMLMetadataType
from core.nlp_processor.v2.jobs.processors.families.html_metadata._template import ExtractHTMLMetadataProcessorTemplate


def make_html_metadata_processor(metadata_type: HTMLMetadataType):

    class ExtractHTMLMetadataProcessor(ExtractHTMLMetadataProcessorTemplate):
        async def process(self) -> Optional[str]:
            tag = self.soup.find("meta", attrs={"name": metadata_type.value})
            return tag.get("content") if tag else None

    ExtractHTMLMetadataProcessor.__name__ = f"ExtractHTMLMetadata{metadata_type.name}Processor"
    return ExtractHTMLMetadataProcessor