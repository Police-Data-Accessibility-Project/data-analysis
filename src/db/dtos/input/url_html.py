from pydantic import BaseModel


class URLHTMLInput(BaseModel):
    url_id: int
    html: str