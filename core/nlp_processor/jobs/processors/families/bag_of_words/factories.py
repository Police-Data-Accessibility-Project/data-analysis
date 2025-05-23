from core.nlp_processor.jobs.processors.families.bag_of_words._template import ExtractHTMLBagOfWordsProcessorTemplate
from core.nlp_processor.jobs.enums import HTMLBagOfWordsJobType

def make_nlp_bag_of_words_entity_processor(
    type_: HTMLBagOfWordsJobType,
    named_entities: list[str]
):

    class ExtractHTMLBagOfWordsNLPEntityProcessor(ExtractHTMLBagOfWordsProcessorTemplate):
        async def process(self) -> dict[str, int]:
            bag_of_words = {}
            for ent in self.spacy_doc.ents:
                if ent.label_ in named_entities:
                    bag_of_words[ent.text] = bag_of_words.get(ent.text, 0) + 1
            return bag_of_words

    title = type_.name.title().replace('_', '')
    ExtractHTMLBagOfWordsNLPEntityProcessor.__name__ = f"ExtractHTMLBagOfWordsNLPProcessor{title}"

    return ExtractHTMLBagOfWordsNLPEntityProcessor

def make_nlp_bag_of_words_part_of_speech_processor(
    type_: HTMLBagOfWordsJobType,
    part_of_speech: str
):

    class ExtractHTMLBagOfWordsNLPPartOfSpeechProcessor(ExtractHTMLBagOfWordsProcessorTemplate):
        async def process(self) -> dict[str, int]:
            bag_of_words = {}
            for token in self.spacy_doc:
                if token.pos_ == part_of_speech:
                    text = token.lemma_
                    bag_of_words[text] = bag_of_words.get(text, 0) + 1
            return bag_of_words

    title = type_.name.title().replace('_', '')
    ExtractHTMLBagOfWordsNLPPartOfSpeechProcessor.__name__ = f"ExtractHTMLBagOfWordsNLPProcessor{title}"

    return ExtractHTMLBagOfWordsNLPPartOfSpeechProcessor