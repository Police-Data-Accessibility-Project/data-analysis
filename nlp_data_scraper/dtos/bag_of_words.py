from typing import Optional, Dict

from pydantic import BaseModel


class BagOfWords(BaseModel):
    all: Optional[dict] = None
    links: Optional[dict] = None
    headers: Optional[Dict[str, Dict[str, int]]] = None
    non_links_non_headers: Optional[dict] = None
