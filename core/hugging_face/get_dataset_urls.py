"""
Get URLs from a given dataset and add them to the database
"""
import asyncio

from datasets import load_dataset

from core.database_logic.database_client import DatabaseClient


def load_urls_from_huggingface(dataset_name: str) -> list[str]:
    ds = load_dataset(dataset_name)
    urls = []
    for row in ds['train']:
        url = row["url"]
        if url is None:
            continue
        urls.append(url)
    return urls


if __name__ == "__main__":
    urls = load_urls_from_huggingface("PDAP/training-urls")
    dbc = DatabaseClient()
    asyncio.run(dbc.add_urls(urls))
