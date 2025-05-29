"""
Builds queries for obtaining data to be ingested into an ML model
"""


class QueryBuilder:


    async def aggregates(self):
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

        pass

    async def bag_of_words(self):
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
        pass

    async def bag_of_tags(self):
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

    async def tag_term_matrix(self):
        """
        Creates a query for generating a tag term matrix
        :return:
        """
        pass