from sqlalchemy import select, func, ColumnElement

from src.db.models.core import URLCompressedHTML


class DuplicateHashCTE:
    """
    Hashes of URL html content shared between more than one URL
    """
    def __init__(self):
        self.query = (
            select(
                URLCompressedHTML.hash
            )
            .having(func.count(URLCompressedHTML.id) > 1)
            .group_by(URLCompressedHTML.hash)
            .cte("duplicate_hash")
        )

    @property
    def hash(self) -> ColumnElement[str]:
        return self.query.c.hash