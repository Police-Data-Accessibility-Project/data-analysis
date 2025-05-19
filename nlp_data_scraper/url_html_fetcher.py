import asyncio
import random

from aiohttp import ClientSession, ClientError


class URLHTMLFetcher:
    
    def __init__(
        self, 
        session: ClientSession,
        timeout: int = 20,
        max_retries: int = 5
    ):
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = session
        
    async def fetch_html(self, url: str) -> str:
        attempt = 0

        while True:
            try:
                async with self.session.get(url, timeout=self.timeout) as response:
                    response.raise_for_status()
                    return await response.text()

            except (ClientError, asyncio.TimeoutError) as e:
                if attempt >= self.max_retries:
                    raise RuntimeError(f"Failed to fetch {url} after {self.max_retries} attempts") from e

                backoff = (2 ** attempt) + random.uniform(0, 1)
                attempt += 1
                await asyncio.sleep(backoff)