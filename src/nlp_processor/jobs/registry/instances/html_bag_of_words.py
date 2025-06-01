from src.nlp_processor.jobs.identifiers.implementations import HTMLBagOfWordsJobIdentifier
from src.nlp_processor.jobs.enums import HTMLBagOfWordsJobType
from src.nlp_processor.jobs.processors.families.html_bag_of_tags.implementations import \
    ExtractHTMLBagOfWordsAllTagsProcessor
from src.nlp_processor.jobs.processors.families.html_bag_of_words.implementations import \
    ExtractHTMLBagOfWordsAllWordsProcessor, ExtractHTMLBagOfWordsLocationsProcessor, \
    ExtractHTMLBagOfWordsCommonNounsProcessor, ExtractHTMLBagOfWordsPersonsProcessor, \
    ExtractHTMLBagOfWordsVerbsProcessor, ExtractHTMLBagOfWordsProperNounsProcessor, \
    ExtractHTMLBagOfWordsAdverbsProcessor, ExtractHTMLBagOfWordsAdjectivesProcessor
from src.nlp_processor.jobs.registry.entry import JobRegistryEntry

def get_identifier(job_type: HTMLBagOfWordsJobType) -> HTMLBagOfWordsJobIdentifier:
    return HTMLBagOfWordsJobIdentifier(job_type=job_type)

HTML_BAG_OF_WORDS_JOBS = [
    JobRegistryEntry(
        identifier=get_identifier(HTMLBagOfWordsJobType.ALL_WORDS),
        processor=ExtractHTMLBagOfWordsAllWordsProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLBagOfWordsJobType.LOCATIONS),
        processor=ExtractHTMLBagOfWordsLocationsProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLBagOfWordsJobType.PERSONS),
        processor=ExtractHTMLBagOfWordsPersonsProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLBagOfWordsJobType.COMMON_NOUNS),
        processor=ExtractHTMLBagOfWordsCommonNounsProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLBagOfWordsJobType.PROPER_NOUNS),
        processor=ExtractHTMLBagOfWordsProperNounsProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLBagOfWordsJobType.VERBS),
        processor=ExtractHTMLBagOfWordsVerbsProcessor,
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLBagOfWordsJobType.ADJECTIVES),
        processor=ExtractHTMLBagOfWordsAdjectivesProcessor
    ),
    JobRegistryEntry(
        identifier=get_identifier(HTMLBagOfWordsJobType.ADVERBS),
        processor=ExtractHTMLBagOfWordsAdverbsProcessor
    )
]