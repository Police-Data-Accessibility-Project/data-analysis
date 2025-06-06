from src.nlp_processor.jobs.enums import HTMLBagOfTagsJobType
from src.nlp_processor.jobs.identifiers.implementations import HTMLBagOfTagsJobIdentifier
from src.nlp_processor.jobs.processors.families.html_bag_of_tags.implementations import \
    ExtractHTMLBagOfWordsAllTagsProcessor
from src.nlp_processor.jobs.registry.entry import JobRegistryEntry

HTML_BAG_OF_TAGS_JOBS = [
    JobRegistryEntry(
        identifier=HTMLBagOfTagsJobIdentifier(job_type=HTMLBagOfTagsJobType.ALL_TAGS),
        processor=ExtractHTMLBagOfWordsAllTagsProcessor
    ),
]