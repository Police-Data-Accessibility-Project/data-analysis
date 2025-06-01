from collections import Counter

from src.nlp_processor.jobs.processors.families.html_bag_of_tags._template import ExtractHTMLBagOfTagsProcessorTemplate

class ExtractHTMLBagOfWordsAllTagsProcessor(ExtractHTMLBagOfTagsProcessorTemplate):
    async def process(self) -> dict[str, int]:
        tag_names = [tag.name for tag in self.soup.find_all(True)]
        if len(tag_names) == 0:
            return {}
        return dict(Counter(tag_names))
