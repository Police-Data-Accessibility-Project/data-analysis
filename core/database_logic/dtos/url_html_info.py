from pydantic import BaseModel


class URLHTMLInfo(BaseModel):
    url_id: int
    html: str