from collections import Counter
from typing import Dict

import spacy
from spacy.tokens import Doc

from core.nlp_processor.dtos.page_info import PageInfo


class PageNLPDataProcessor:

    def __init__(self, page_info: PageInfo, n_most_common_words: int = 100):
        self.page_info = page_info
        self.n_most_common_words = n_most_common_words
        self.nlp = spacy.load('en_core_web_sm')

    def remove_proper_nouns(self, text: str) -> str:
        doc = self.nlp(text)

        # Keep tokens that are not proper nouns
        filtered_tokens = [token.text for token in doc if token.pos_ != "PROPN"]

        # Reconstruct text with spaces and punctuation
        return Doc(doc.vocab, words=filtered_tokens).text

    def tokenize_spacy(self, text: str) -> Counter:
        doc = self.nlp(text.lower())

        lemmatized = [
            token.lemma_
            for token in doc
            if token.is_alpha  # keep alphabetic only
               and not token.is_stop  # remove stopwords
               and len(token.lemma_) > 1  # remove single-letter lemmas
        ]

        return Counter(lemmatized)

    def get_bag_of_words(self, text: str) -> Dict[str, int]:
        text_without_proper_nouns = self.remove_proper_nouns(text)
        c: Counter = self.tokenize_spacy(text_without_proper_nouns)
        d = {}
        for word, count in c.most_common(self.n_most_common_words):
            d[word] = count
        return d
