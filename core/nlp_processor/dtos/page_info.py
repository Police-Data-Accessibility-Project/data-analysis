from typing import Optional, Dict

from pydantic import BaseModel


class PageInfo(BaseModel):
    title: Optional[str]
    description: Optional[str]
    keywords: Optional[str]
    all_text: str
    link_text: str
    header_texts: Dict[str, str]
    non_link_non_header_text: str
    tag_counts: Dict[str, int]
