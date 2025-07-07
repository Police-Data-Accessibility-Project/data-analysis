from typing_extensions import override

import polars as pl
from sqlalchemy import select, ColumnElement, func, Float, cast, and_
from sqlalchemy.orm import InstrumentedAttribute

from src.db.df_labels.bag_of_words import BagOfWordsBaseLabels
from src.db.format import rows_to_list_of_simple_dicts
from src.db.models.core import HTMLBagOfWords, URLAnnotations, URL, HTMLTerm
from src.db.queries.builder import QueryBuilderBase
from src.db.queries.ml_input_builder.bag_of_words_.ctes.count_all_terms_in_doc import CountAllTermsInDocCTE
from src.db.queries.ml_input_builder.bag_of_words_.ctes.count_docs_with_term import CountDocsWithTermCTE
from src.db.queries.ml_input_builder.bag_of_words_.ctes.relevant_urls import RelevantURLsCTE
from src.db.queries.ml_input_builder.bag_of_words_.ctes.tf_idf import TfIdfCTE
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
    async def run(self) -> pl.DataFrame:
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

        tf_idf_cte = TfIdfCTE(
            count_all_docs=count_all_docs,
            count_all_terms_in_doc=count_all_terms_in_doc,
            count_docs_with_terms_cte=count_docs_with_terms_cte,
            url_term_cross_join_cte=url_term_cross_join_cte,
            bag_of_words_type=self.bag_of_words_type
        )

        # Add annotations
        labels = BagOfWordsBaseLabels()

        final_query = (
            select(
                URL.url.label("url"),
                HTMLTerm.name.label("term"),
                tf_idf_cte.tf_idf.label(labels.tf_idf),
                URLAnnotations.relevant.label(labels.relevant),
                URLAnnotations.record_type_fine.label(labels.record_type_fine),
                URLAnnotations.record_type_coarse.label(labels.record_type_coarse)
            ).join(
                URLAnnotations,
                URLAnnotations.url_id == tf_idf_cte.url_id,
            )
            .join(
                URL,
                URL.id == tf_idf_cte.url_id
            )
            .join(
                HTMLTerm,
                HTMLTerm.id == tf_idf_cte.term_id
            )
        )

        result = await self.execute_all(query=final_query)

        return pl.DataFrame(rows_to_list_of_simple_dicts(result))
