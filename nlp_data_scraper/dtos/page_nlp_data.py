from pydantic import BaseModel

from nlp_data_scraper.dtos.bag_of_words import BagOfWords
from nlp_data_scraper.dtos.page_tag_counts import PageTagCounts


class PageNLPData(BaseModel):
    bag_of_words: BagOfWords
    tag_counts: PageTagCounts