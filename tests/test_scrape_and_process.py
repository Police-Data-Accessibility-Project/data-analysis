import pytest
from aiohttp import ClientSession

from bag_of_words_extractor.html_extractor import HTMLExtractor
from bag_of_words_extractor.page_nlp_data_processor import PageNLPDataProcessor
from bag_of_words_extractor.url_html_fetcher import URLHTMLFetcher


@pytest.mark.asyncio
async def test_scrape_and_process():
    url = "https://www.scrapethissite.com/pages/simple/"
    async with ClientSession() as session:
        fetcher = URLHTMLFetcher(session)
        html = await fetcher.fetch_html(url)
    extractor = HTMLExtractor(html)
    page_info = extractor.get_page_info()
    processor = PageNLPDataProcessor(page_info)
    page_nlp_data = processor.process()
    print(page_nlp_data)
