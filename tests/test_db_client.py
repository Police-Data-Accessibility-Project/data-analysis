import pytest

from src.db.client import DatabaseClient


@pytest.mark.asyncio
async def test_get_bag_of_words_for_ml():
    dbc = DatabaseClient()
    result = await dbc.get_bag_of_words_for_ml()
    assert result