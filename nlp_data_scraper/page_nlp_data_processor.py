from collections import Counter
from typing import Dict

import spacy
from spacy.tokens import Doc

from nlp_data_scraper.dtos.bag_of_words import BagOfWords
from nlp_data_scraper.dtos.page_info import PageInfo
from nlp_data_scraper.dtos.page_nlp_data import PageNLPData
from nlp_data_scraper.dtos.page_tag_counts import PageTagCounts


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

    def process(self) -> PageNLPData:
        return PageNLPData(
            bag_of_words=BagOfWords(
                all=self.get_bag_of_words(self.page_info.all_text),
                links=self.get_bag_of_words(self.page_info.link_text),
                headers={
                    h: self.get_bag_of_words(self.page_info.header_texts[h])
                    for h in self.page_info.header_texts
                },
                non_links_non_headers=self.get_bag_of_words(self.page_info.non_link_non_header_text)
            ),
            tag_counts=PageTagCounts(
                img=self.page_info.tag_counts.get('img', 0),
                a=self.page_info.tag_counts.get('a', 0),
                p=self.page_info.tag_counts.get('p', 0),
                span=self.page_info.tag_counts.get('span', 0),
                div=self.page_info.tag_counts.get('div', 0),
                li=self.page_info.tag_counts.get('li', 0),
                ul=self.page_info.tag_counts.get('ul', 0),
                ol=self.page_info.tag_counts.get('ol', 0),
                table=self.page_info.tag_counts.get('table', 0),
                tr=self.page_info.tag_counts.get('tr', 0),
                td=self.page_info.tag_counts.get('td', 0),
                th=self.page_info.tag_counts.get('th', 0),
                h1=self.page_info.tag_counts.get('h1', 0),
                h2=self.page_info.tag_counts.get('h2', 0),
                h3=self.page_info.tag_counts.get('h3', 0),
                h4=self.page_info.tag_counts.get('h4', 0),
                h5=self.page_info.tag_counts.get('h5', 0),
                h6=self.page_info.tag_counts.get('h6', 0),
                form=self.page_info.tag_counts.get('form', 0),
                input=self.page_info.tag_counts.get('input', 0),
                button=self.page_info.tag_counts.get('button', 0),
                meta=self.page_info.tag_counts.get('meta', 0),
            )
        )