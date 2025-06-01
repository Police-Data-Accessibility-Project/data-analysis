"""
Formats results into an ML-ingestable format.
"""
import asyncio

import joblib
import pandas as pd

from src.db.client import DatabaseClient
from src.db.dtos.labeled_data_frame import LabeledDataFrame
from src.ml_input_builder.formatter import Formatter
from src.ml_input_builder.query_builder import QueryBuilder
from src.utils.paths import get_output_path


class MLInputBuilder:
    """
    Formats results into an ML-ingestable format.
    """

    def __init__(self):
        self.query_builder = QueryBuilder()
        self.db_client = DatabaseClient()
        self.formatter = Formatter()


    @staticmethod
    async def save(
        name: str,
        dict_: dict,
    ):
        joblib.dump(
            value=dict_,
            filename=get_output_path(f"{name}.joblib")
        )


    async def bag_of_words(self):
        ldf: LabeledDataFrame = await self.db_client.get_bag_of_words_for_ml()

        intermediate = await self.formatter.bag_of_words(ldf)

        await self.save(
            name="bag_of_words",
            dict_=intermediate.model_dump(),
        )

if __name__ == "__main__":
    ml_input_builder = MLInputBuilder()
    asyncio.run(ml_input_builder.bag_of_words())