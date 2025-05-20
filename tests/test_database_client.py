import pytest

from core.database_logic.database_client import DatabaseClient


@pytest.mark.asyncio
async def test_get_next_valid_url_for_nlp_preprocessing():
    dbc = DatabaseClient()
    result = await dbc.get_next_valid_url_batch_for_nlp_preprocessing()
    print(result)