from typing import Callable, Optional

from core.nlp_processor.jobs.processors.families.url_component._template import ExtractURLComponentProcessorTemplate
from core.nlp_processor.jobs.enums import URLComponentJobType


def make_url_component_processor(
    type_: URLComponentJobType,
    extractor: Callable[[str], Optional[str]]
) -> type:
    class Processor(ExtractURLComponentProcessorTemplate):
        async def process(self) -> Optional[str]:
            return extractor(self.url)

    Processor.__name__ = f"ExtractURL{type_.name}Processor"
    return Processor
