from typing import Optional

from src.nlp_processor.jobs.enums import HTMLMetadataJobType
from src.nlp_processor.jobs.processors.families.html_metadata._template import ExtractHTMLMetadataProcessorTemplate


def make_html_metadata_processor(metadata_type: HTMLMetadataJobType):

    class ExtractHTMLMetadataProcessor(ExtractHTMLMetadataProcessorTemplate):
        async def process(self) -> Optional[str]:
            tag = self.soup.find("meta", attrs={"name": metadata_type.value})
            return tag.get("content") if tag else None

    ExtractHTMLMetadataProcessor.__name__ = f"ExtractHTMLMetadata{metadata_type.name}Processor"
    return ExtractHTMLMetadataProcessor