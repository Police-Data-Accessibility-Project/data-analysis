from sqlalchemy import select, exists, literal, ColumnElement

from src.db.models.core import URL, HTMLBagOfWords
from src.db.queries.ml_input_builder.bag_of_words_.ctes.whitelisted_urls import WhitelistedURLsCTE
from src.nlp_processor.jobs.enums import HTMLBagOfWordsJobType


class RelevantURLsCTE:

    def __init__(
        self,
        bag_of_words_type: HTMLBagOfWordsJobType,
        whitelisted_urls_cte: WhitelistedURLsCTE
    ):
        self.query = (
            select(whitelisted_urls_cte.url_id)
            .where(
                exists(
                    select(literal(1))
                    .where(
                        HTMLBagOfWords.type == bag_of_words_type.value,
                        HTMLBagOfWords.url_id == whitelisted_urls_cte.url_id,
                    )
                )
            )
            .cte("relevant_urls")
        )

    @property
    def url_id(self) -> ColumnElement[int]:
        return self.query.c.id