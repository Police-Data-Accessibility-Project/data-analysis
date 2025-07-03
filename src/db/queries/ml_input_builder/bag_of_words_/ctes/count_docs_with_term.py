from sqlalchemy import select, func, ColumnElement

from src.db.models.core import HTMLBagOfWords
from src.db.queries.ml_input_builder.bag_of_words_.ctes.top_n_terms import TopNTermsCTE
from src.nlp_processor.jobs.enums import HTMLBagOfWordsJobType


class CountDocsWithTermCTE:

    def __init__(
        self,
        top_n_terms: TopNTermsCTE,
        bag_of_words_type: HTMLBagOfWordsJobType
    ):
        self.query = (
            select(
                top_n_terms.term_id.label("term_id"),
                func.count(HTMLBagOfWords.url_id).label("term_count")
            )
            .join(
                HTMLBagOfWords,
                HTMLBagOfWords.term_id == top_n_terms.term_id
            )
            .where(HTMLBagOfWords.type == bag_of_words_type.value)
            .group_by(top_n_terms.term_id)
            .cte("term_counts")
        )

    @property
    def term_id(self) -> ColumnElement[int]:
        return self.query.c.term_id

    @property
    def term_count(self) -> ColumnElement[int]:
        return self.query.c.term_count
