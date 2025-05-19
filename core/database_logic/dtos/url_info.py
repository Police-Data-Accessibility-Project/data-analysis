from pydantic import BaseModel


class URLInfo(BaseModel):
    id: int
    url: str