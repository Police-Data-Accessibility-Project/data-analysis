from sqlalchemy import select, exists, literal, ColumnElement

from src.db.models.core import URL, HTMLBagOfWords
from src.nlp_processor.jobs.enums import HTMLBagOfWordsJobType


class RelevantURLsCTE:

    def __init__(
        self,
        bag_of_words_type: HTMLBagOfWordsJobType
    ):
        self.query = (
            select(URL.id)
            .where(
                exists(
                    select(literal(1))
                    .where(
                        HTMLBagOfWords.type == bag_of_words_type.value,
                        HTMLBagOfWords.url_id == URL.id,
                    )
                )
            )
            .cte("relevant_urls")
        )

    @property
    def url_id(self) -> ColumnElement[int]:
        return self.query.c.id