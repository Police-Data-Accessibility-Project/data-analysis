from core.nlp_processor.jobs.enums import HTMLBagOfWordsJobType
from core.nlp_processor.jobs.processors.families.html_bag_of_words._template import \
    ExtractHTMLBagOfWordsProcessorTemplate
from core.nlp_processor.jobs.processors.families.html_bag_of_words.factories import \
    make_nlp_bag_of_words_entity_processor, make_nlp_bag_of_words_part_of_speech_processor

ExtractHTMLBagOfWordsLocationsProcessor = make_nlp_bag_of_words_entity_processor(
    type_=HTMLBagOfWordsJobType.LOCATIONS,
    named_entities=['GPE', 'LOC', 'FAC']
)

ExtractHTMLBagOfWordsPersonsProcessor = make_nlp_bag_of_words_entity_processor(
    type_=HTMLBagOfWordsJobType.PERSONS,
    named_entities=['PERSON']
)

ExtractHTMLBagOfWordsCommonNounsProcessor = make_nlp_bag_of_words_part_of_speech_processor(
    type_=HTMLBagOfWordsJobType.COMMON_NOUNS,
    part_of_speech="NOUN"
)

ExtractHTMLBagOfWordsProperNounsProcessor = make_nlp_bag_of_words_part_of_speech_processor(
    type_=HTMLBagOfWordsJobType.PROPER_NOUNS,
    part_of_speech="PROPN"
)

ExtractHTMLBagOfWordsVerbsProcessor = make_nlp_bag_of_words_part_of_speech_processor(
    type_=HTMLBagOfWordsJobType.VERBS,
    part_of_speech="VERB"
)

ExtractHTMLBagOfWordsAdjectivesProcessor = make_nlp_bag_of_words_part_of_speech_processor(
    type_=HTMLBagOfWordsJobType.ADJECTIVES,
    part_of_speech="ADJ"
)

ExtractHTMLBagOfWordsAdverbsProcessor = make_nlp_bag_of_words_part_of_speech_processor(
    type_=HTMLBagOfWordsJobType.ADVERBS,
    part_of_speech="ADV"
)

class ExtractHTMLBagOfWordsAllWordsProcessor(ExtractHTMLBagOfWordsProcessorTemplate):
    async def process(self) -> dict[str, int]:
        bag_of_words = {}
        for token in self.spacy_doc:
            if token.is_stop:
                continue
            if not token.is_alpha:
                continue
            text = token.lemma_.lower()
            bag_of_words[text] = bag_of_words.get(text, 0) + 1
        return bag_of_words
