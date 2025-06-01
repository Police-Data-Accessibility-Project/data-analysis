from pydantic import BaseModel


class URLOutput(BaseModel):
    id: int
    url: str