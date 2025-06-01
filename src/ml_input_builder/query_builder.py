"""
Builds queries for obtaining data to be ingested into an ML model
"""
from sqlalchemy import select, func, Select

from src.db.models.core import URL, URLAnnotations, HTMLBagOfWords, HTMLTerm
from src.nlp_processor.jobs.enums import HTMLBagOfWordsJobType


class QueryBuilder:


    async def aggregates(self) -> Select:
        """
        Creates a query for retrieving various data aggregate counts.

        Provides the following columns:

        - url_id (integer; used for reference)
        - relevancy annotation (class)
        - record_type_fine annotation (class)
        - record_type_coarse annotation (class)
        - all_words_count (integer)
        - locations_count (integer)
        - persons_count (integer)
        - common_nouns_count (integer)
        - proper_nouns_count (integer)
        - verbs_count (integer)
        - adjectives_count (integer)
        - adverbs_count (integer)
        - all_tags_count (integer)

        :return:
        """
        # TODO: Under construction
        #
        # count_functions = []
        # for val in HTMLBagOfWordsJobType:
        #     cte = (
        #         select(
        #     )
        #
        #     count_function = (
        #         func.sum(
        #             HTMLBagOfWords.count
        #         ).filter(
        #             HTMLBagOfWords.type == val.value
        #         ).label(f"{val.value}_count")
        #     )
        #     count_functions.append(count_function)
        #
        # query = (
        #     select(
        #         URL.id,
        #         URLAnnotations.relevant,
        #         URLAnnotations.record_type_fine,
        #         URLAnnotations.record_type_coarse,
        #     )
        # )


    async def bag_of_words(self) -> Select:
        """
        Creates a query for retrieving bag of words data

        Provides the following columns:

        - url_id (integer; used for reference)
        - relevancy annotation (class)
        - record_type_fine annotation (class)
        - record_type_coarse annotation (class)
        - a series of columns for each word, each representing a count (integer)

        :return:
        """
        return (
            select(
                HTMLBagOfWords.url_id,
                HTMLTerm.name,
                HTMLBagOfWords.count,
                URLAnnotations.relevant,
                URLAnnotations.record_type_fine,
                URLAnnotations.record_type_coarse,
            )
            .join(
                HTMLTerm,
                HTMLBagOfWords.term_id == HTMLTerm.id
            )
            .join(
                URLAnnotations,
                URLAnnotations.url_id == HTMLBagOfWords.url_id
            )
            .where(
                HTMLBagOfWords.type == HTMLBagOfWordsJobType.COMMON_NOUNS
            )
        )

    async def bag_of_tags(self) -> Select:
        """
        Creates a query for retrieving bag of tags data

        Provides the following columns:

        - url_id (integer; used for reference)
        - relevancy annotation (class)
        - record_type_fine annotation (class)
        - record_type_coarse annotation (class)
        - a series of columns for each tag, each representing a count (integer)
        :return:
        """
        pass

    async def tag_term_matrix(self) -> Select:
        """
        Creates a query for generating a tag term matrix
        :return:
        """
        pass