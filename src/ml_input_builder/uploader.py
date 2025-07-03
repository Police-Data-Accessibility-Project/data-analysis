from environs import Env
from huggingface_hub import HfApi

from src.ml_input_builder.constants import DATA_OUTPUT_PATH
from src.ml_input_builder.registry.entry import DatasetRegistryEntry


class HuggingFaceUploader:
    """Uploads data to HuggingFace"""

    def __init__(
        self,
        token: str
    ):
        env = Env()
        env.read_env()
        self.api = HfApi(
            token=token
        )

    def upload(self, entry: DatasetRegistryEntry):
        self.api.upload_file(
            path_or_fileobj=f"{DATA_OUTPUT_PATH}{entry.filename}",
            path_in_repo=entry.filename,
            repo_id=entry.repo_id,
            repo_type="dataset",
        )