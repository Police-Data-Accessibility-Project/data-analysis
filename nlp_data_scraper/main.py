import asyncio
from typing import Optional

from aiohttp import ClientSession
from datasets import load_dataset
from pydantic import BaseModel
from simple_state_tracker import KeyModel, DataModel, SimpleStateTracker
from tqdm.asyncio import tqdm_asyncio

from nlp_data_scraper.dtos.page_nlp_data import PageNLPData
from nlp_data_scraper.html_extractor import HTMLExtractor
from nlp_data_scraper.page_nlp_data_processor import PageNLPDataProcessor
from nlp_data_scraper.url_html_fetcher import URLHTMLFetcher


class ScrapeAndProcessResult(BaseModel):
    page_nlp_data: Optional[PageNLPData] = None
    error: Optional[str] = None


semaphore = asyncio.Semaphore(10)

class Key(KeyModel):
    url: str

class Data(DataModel):
    result: Optional[ScrapeAndProcessResult] = None

def load_urls_from_huggingface() -> SimpleStateTracker[Key, Data]:
    ds = load_dataset("PDAP/training-urls")
    sst = SimpleStateTracker(key_model=Key, data_model=Data, path="url_state.json")
    for row in ds['train']:
        url = row["url"]
        if url is None:
            continue
        sst.set(Key(url=url), Data())

    return sst

async def limited_scrape_and_process(url: str, fetcher: URLHTMLFetcher) -> ScrapeAndProcessResult:
    async with semaphore:
        return await scrape_and_process(url, fetcher)

async def scrape_and_process(url: str, fetcher: URLHTMLFetcher) -> ScrapeAndProcessResult:
    try:
        html = await fetcher.fetch_html(url)
    except Exception as e:
        return ScrapeAndProcessResult(error=f"{type(e).__name__}: {e}")
    extractor = HTMLExtractor(html)
    page_info = extractor.get_page_info()
    processor = PageNLPDataProcessor(page_info)
    page_nlp_data = processor.process()
    return ScrapeAndProcessResult(page_nlp_data=page_nlp_data)


async def scrape_nlp_data(sst: SimpleStateTracker[Key, Data]):
    keys = sst.all_keys()
    urls = [key.url for key in keys]
    async with ClientSession() as session:
        fetcher = URLHTMLFetcher(session)
        results: list[ScrapeAndProcessResult] = await tqdm_asyncio.gather(
            *[
                asyncio.create_task(
                    limited_scrape_and_process(url, fetcher)
                )
                for url in urls]
        )

    for result, key in zip(results, keys):
        with sst.edit(key) as data:
            data.result = result




if __name__ == "__main__":
    sst = load_urls_from_huggingface()
    asyncio.run(scrape_nlp_data(sst))
    sst.save()