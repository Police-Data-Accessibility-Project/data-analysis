from sqlalchemy import select, func, ColumnElement

from src.db.models.core import HTMLBagOfWords
from src.nlp_processor.jobs.enums import HTMLBagOfWordsJobType


class CountAllTermsInDocCTE:
    def __init__(
        self,
        relevant_url_id_col: ColumnElement[int],
        bag_of_words_type: HTMLBagOfWordsJobType,
        min_doc_term_threshold: int
    ):
        sum_func = func.sum(HTMLBagOfWords.count)
        self.query = (
            select(
                relevant_url_id_col.label("url_id"),
                sum_func.label("doc_term_count")
            )
            .join(
                HTMLBagOfWords,
                HTMLBagOfWords.url_id == relevant_url_id_col
            )
            .where(HTMLBagOfWords.type == bag_of_words_type.value)
            .having(sum_func > min_doc_term_threshold)
            .group_by(relevant_url_id_col)
            .cte("doc_term_counts")
        )

    @property
    def url_id(self) -> ColumnElement[int]:
        return self.query.c.url_id

    @property
    def doc_term_count(self) -> ColumnElement[int]:
        return self.query.c.doc_term_count