"""
Fetch HTML from URLs
"""

import asyncio

from aiohttp import ClientSession, ClientResponseError
from tqdm import tqdm
from yarl import URL

from src.db.client import DatabaseClient
from src.db.enums import ErrorType
from src.html_fetcher.core import URLHTMLFetcher
from src.utils.exception import format_exception


async def main():
    dbc = DatabaseClient()
    url_infos = await dbc.get_urls_without_response_codes()
    async with ClientSession() as session:
        fetcher = URLHTMLFetcher(session)
        for url_info in tqdm(url_infos):
            if url_info.url.endswith('.csv'):
                continue
            if url_info.url.endswith('.json'):
                continue
            if url_info.url.endswith('.xml'):
                continue
            if url_info.url.endswith('.pdf'):
                continue
            try:
                html = await fetcher.fetch_html(url_info.url)
                await dbc.add_html(
                    url_id=url_info.id,
                    html=html
                )
                await dbc.update_response_code(
                    url_id=url_info.id,
                    response_code=200
                )
            except ClientResponseError as e:
                code = e.status
                await dbc.update_response_code(
                    url_id=url_info.id,
                    response_code=code
                )
            except Exception as e:
                msg = format_exception(e)
                await dbc.add_url_error(
                    url_id=url_info.id,
                    error=msg,
                    error_type=ErrorType.SCRAPE
                )




if __name__ == "__main__":
    asyncio.run(main())