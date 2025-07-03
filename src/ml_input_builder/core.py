"""
Formats results into an ML-ingestable format.
"""

from src.db.client import DatabaseClient
from src.ml_input_builder.registry.instantiations import BAG_OF_WORDS_REGISTRY_ENTRY, RAW_REGISTRY_ENTRY
from src.ml_input_builder.uploader import HuggingFaceUploader
from src.ml_input_builder.write import write_to_parquet


class MLInputBuilder:
    """
    Formats results into an ML-ingestable format.
    """

    def __init__(
        self,
        huggingface_token: str
    ):
        self.db_client = DatabaseClient()
        self.uploader = HuggingFaceUploader(
            token=huggingface_token
        )



    async def bag_of_words(self):
        df = await self.db_client.get_bag_of_words_for_ml()

        write_to_parquet(
            df,
            name=BAG_OF_WORDS_REGISTRY_ENTRY.filename
        )

        self.uploader.upload(
            entry=BAG_OF_WORDS_REGISTRY_ENTRY
        )

    async def raw(self):
        df = await self.db_client.get_raw_for_ml()

        write_to_parquet(
            df,
            name=RAW_REGISTRY_ENTRY.filename
        )

        self.uploader.upload(
            entry=RAW_REGISTRY_ENTRY
        )


