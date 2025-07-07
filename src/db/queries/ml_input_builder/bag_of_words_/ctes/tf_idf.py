from sqlalchemy import func, Float, cast, select, and_, ColumnElement
from sqlalchemy.orm import InstrumentedAttribute

from src.db.models.core import HTMLBagOfWords
from src.db.queries.ml_input_builder.bag_of_words_.ctes.count_all_terms_in_doc import CountAllTermsInDocCTE
from src.db.queries.ml_input_builder.bag_of_words_.ctes.count_docs_with_term import CountDocsWithTermCTE
from src.db.queries.ml_input_builder.bag_of_words_.ctes.url_term_cross_join import URLTermCrossJoinCTE
from src.nlp_processor.jobs.enums import HTMLBagOfWordsJobType


class TfIdfCTE:

    def __init__(
        self,
        count_all_docs: int,
        count_all_terms_in_doc: CountAllTermsInDocCTE,
        count_docs_with_terms_cte: CountDocsWithTermCTE,
        url_term_cross_join_cte: URLTermCrossJoinCTE,
        bag_of_words_type: HTMLBagOfWordsJobType
    ):
        count_term_in_doc_col: InstrumentedAttribute[int] = HTMLBagOfWords.count
        tf = count_term_in_doc_col / count_all_terms_in_doc.doc_term_count
        idf = func.log(
            count_all_docs /
            func.coalesce(count_docs_with_terms_cte.term_count, 1)  # Account for nulls in join
        )
        tf_idf = cast(tf * idf, Float)

        self.query = (
            select(
                url_term_cross_join_cte.url_id.label("url_id"),
                url_term_cross_join_cte.term_id.label("term_id"),
                # Below used for debugging
                # func.coalesce(count_term_in_doc_col, 0).label("count_term_in_doc"),
                # count_all_terms_in_doc_col.label("count_all_terms_in_doc"),
                # literal(count_all_docs).label("count_all_documents"),
                # count_docs_with_term_col.label("count_docs_with_term"),
                # tf.label("tf"),
                # idf.label("idf"),
                tf_idf.label("tf_idf")
            )
            .outerjoin(
                HTMLBagOfWords,
                and_(
                    HTMLBagOfWords.url_id == url_term_cross_join_cte.url_id,
                    HTMLBagOfWords.term_id == url_term_cross_join_cte.term_id
                )
            )
            .join(
                count_docs_with_terms_cte.query,
                count_docs_with_terms_cte.term_id == url_term_cross_join_cte.term_id
            )
            .join(
                count_all_terms_in_doc.query,
                count_all_terms_in_doc.url_id == url_term_cross_join_cte.url_id
            )
            .where(
                HTMLBagOfWords.type == bag_of_words_type.value
            )
        ).cte("tf_idf")

    @property
    def term_id(self) -> ColumnElement[int]:
        return self.query.c.term_id

    @property
    def url_id(self) -> ColumnElement[int]:
        return self.query.c.url_id

    @property
    def tf_idf(self) -> ColumnElement[float]:
        return self.query.c.tf_idf
