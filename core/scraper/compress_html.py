import asyncio

import brotli

from core.compression_logic import compress_html
from core.database_logic.database_client import DatabaseClient


async def main():
    dbc = DatabaseClient()
    next_url_html_info = await dbc.get_next_uncompressed_html()
    while next_url_html_info is not None:
        print(f"Compressing URL {next_url_html_info.url_id}...")
        compressed_html = compress_html(next_url_html_info.html)
        await dbc.add_compressed_html(next_url_html_info.url_id, compressed_html)
        next_url_html_info = await dbc.get_next_uncompressed_html()




if __name__ == "__main__":
    asyncio.run(main())