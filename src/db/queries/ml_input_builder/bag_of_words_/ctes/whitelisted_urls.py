from sqlalchemy import select, ColumnElement

from src.db.models.core import URL, URLCompressedHTML
from src.db.queries.ml_input_builder.bag_of_words_.ctes.duplicate_hash_cte import DuplicateHashCTE


class WhitelistedURLsCTE:
    """
    Returns URLs that are whitelisted
    Criterion for whitelisting:
        - URL's hash is not in `duplicate_hash`
    """
    def __init__(
        self,
        duplicate_hash: DuplicateHashCTE
    ):
        self.query = (
            select(URL.id)
            .join(URLCompressedHTML, URL.id == URLCompressedHTML.url_id)
            .where(URLCompressedHTML.hash.notin_(select(duplicate_hash.hash)))
            .cte("whitelisted_urls")
        )

    @property
    def url_id(self) -> ColumnElement[int]:
        return self.query.c.id
