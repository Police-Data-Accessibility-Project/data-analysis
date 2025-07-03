from pydantic import BaseModel


class DatasetRegistryEntry(BaseModel):
    filename: str
    repo_id: str