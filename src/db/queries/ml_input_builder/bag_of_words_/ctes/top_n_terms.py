from sqlalchemy import select, func, ColumnElement

from src.db.models.core import HTMLBagOfWords
from src.nlp_processor.jobs.enums import HTMLBagOfWordsJobType


class TopNTermsCTE:

    def __init__(self, top_n_words: int, bag_of_words_type: HTMLBagOfWordsJobType):
        self.query = (
            select(HTMLBagOfWords.term_id)
            .where(HTMLBagOfWords.type == bag_of_words_type.value)
            .group_by(HTMLBagOfWords.term_id)
            .order_by(func.count(HTMLBagOfWords.url_id).desc())
            .limit(top_n_words)
            .cte("top_n_terms")
        )

    @property
    def term_id(self) -> ColumnElement[int]:
        return self.query.c.term_id