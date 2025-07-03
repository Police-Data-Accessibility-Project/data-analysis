from sqlalchemy import select, literal_column

from src.db.queries.ml_input_builder.bag_of_words_.ctes.relevant_urls import RelevantURLsCTE
from src.db.queries.ml_input_builder.bag_of_words_.ctes.top_n_terms import TopNTermsCTE


class URLTermCrossJoinCTE:

    def __init__(
        self,
        relevant_urls: RelevantURLsCTE,
        top_n_terms: TopNTermsCTE,
    ):
        self.query = (
            select(
                relevant_urls.url_id.label("url_id"),
                top_n_terms.term_id.label("term_id"),
            )
            .select_from(relevant_urls.query)
            .outerjoin(
                top_n_terms.query,
                onclause=literal_column("1=1"),
                full=True
            )
            .cte("url_term_cross_join")
        )

    @property
    def url_id(self):
        return self.query.c.url_id

    @property
    def term_id(self):
        return self.query.c.term_id