from typing import override

from sqlalchemy import CTE, select, exists, literal, ColumnElement, func, literal_column, Float, cast, and_
from sqlalchemy.orm import InstrumentedAttribute
import polars as pl

from src.db.df_labels.bag_of_words import BagOfWordsBaseLabels
from src.db.dtos.labeled_data_frame import LabeledDataFrame
from src.db.models.core import URL, HTMLBagOfWords, URLAnnotations
from src.db.queries.builder import QueryBuilderBase
from src.db.queries.ml_input_builder.bag_of_words_.ctes.count_all_terms_in_doc import CountAllTermsInDocCTE
from src.db.queries.ml_input_builder.bag_of_words_.ctes.count_docs_with_term import CountDocsWithTermCTE
from src.db.queries.ml_input_builder.bag_of_words_.ctes.relevant_urls import RelevantURLsCTE
from src.db.queries.ml_input_builder.bag_of_words_.ctes.top_n_terms import TopNTermsCTE
from src.db.queries.ml_input_builder.bag_of_words_.ctes.url_term_cross_join import URLTermCrossJoinCTE
from src.nlp_processor.jobs.enums import HTMLBagOfWordsJobType


class BagOfWordsMLInputQueryBuilder(QueryBuilderBase):

    def __init__(
        self,
        bag_of_words_type: HTMLBagOfWordsJobType = HTMLBagOfWordsJobType.ALL_WORDS,
        top_n_words: int = 1000,
        min_doc_term_threshold: int = 100
    ):
        super().__init__()
        self.bag_of_words_type = bag_of_words_type
        self.top_n_words = top_n_words
        self.min_doc_term_threshold = min_doc_term_threshold

    def _get_relevant_urls_cte(self) -> RelevantURLsCTE:
        return RelevantURLsCTE(self.bag_of_words_type)

    def _get_top_n_terms_cte(self) -> TopNTermsCTE:
        return TopNTermsCTE(
            top_n_words=self.top_n_words,
            bag_of_words_type=self.bag_of_words_type
        )

    @staticmethod
    def _get_url_term_cross_join_cte(
        relevant_urls_cte: RelevantURLsCTE,
        top_n_terms_cte: TopNTermsCTE
    ) -> URLTermCrossJoinCTE:
        return URLTermCrossJoinCTE(
            relevant_urls=relevant_urls_cte,
            top_n_terms=top_n_terms_cte
        )

    async def _get_count_all_docs(
        self,
        relevant_url_id_col: ColumnElement[int]
    ) -> int:
        """Get Total Number of documents with a Bag Of Words CTE (N)"""
        total_docs_query = (
            select(
                func.count(relevant_url_id_col).label("total_document_count")
            )
        )
        return await self.execute_scalar(total_docs_query)

    async def _get_count_all_terms_in_doc(
        self,
        relevant_url_id_col: ColumnElement[int],
    ) -> CountAllTermsInDocCTE:
        """Get Total Number of documents with a Bag Of Words CTE (N)"""
        return CountAllTermsInDocCTE(
            relevant_url_id_col=relevant_url_id_col,
            bag_of_words_type=self.bag_of_words_type,
            min_doc_term_threshold=self.min_doc_term_threshold
        )


    @override
    async def run(self) -> LabeledDataFrame[BagOfWordsBaseLabels]:
        relevant_urls_cte = self._get_relevant_urls_cte()

        count_all_docs = await self._get_count_all_docs(relevant_urls_cte.url_id)

        top_n_terms_cte = self._get_top_n_terms_cte()

        url_term_cross_join_cte = URLTermCrossJoinCTE(
            relevant_urls=relevant_urls_cte,
            top_n_terms=top_n_terms_cte
        )

        count_docs_with_terms_cte = CountDocsWithTermCTE(
            top_n_terms=top_n_terms_cte,
            bag_of_words_type=self.bag_of_words_type
        )

        count_all_terms_in_doc = await self._get_count_all_terms_in_doc(
            relevant_url_id_col=url_term_cross_join_cte.url_id
        )

        # Consolidate Below ==============
        count_term_in_doc_col: InstrumentedAttribute[int] = HTMLBagOfWords.count

        tf = count_term_in_doc_col / count_all_terms_in_doc.doc_term_count
        idf = func.log(
            count_all_docs /
            func.coalesce(count_docs_with_terms_cte.term_count, 1)  # Account for nulls in join
        )
        tf_idf = cast(tf * idf, Float)


        final_subquery = (
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
                HTMLBagOfWords.type == self.bag_of_words_type.value
            )
        ).subquery("tf_idf")


        tf_idf_term_id: ColumnElement[int] = final_subquery.c.term_id
        tf_idf_url_id: ColumnElement[int] = final_subquery.c.url_id
        tf_idf_value: ColumnElement[float] = final_subquery.c.tf_idf

        # Add annotations
        labels = BagOfWordsBaseLabels()

        final_query = (
            select(
                tf_idf_url_id.label(labels.url_id),
                tf_idf_term_id.label(labels.term_id),
                tf_idf_value.label(labels.tf_idf),
                URLAnnotations.relevant.label(labels.relevant),
                URLAnnotations.record_type_fine.label(labels.record_type_fine),
                URLAnnotations.record_type_coarse.label(labels.record_type_coarse)
            ).join(
                URLAnnotations,
                URLAnnotations.url_id == tf_idf_url_id,
            )
        )

        result = await self.execute_all(query=final_query)

        return LabeledDataFrame(
            df=pl.DataFrame(result),
            labels=labels
        )
