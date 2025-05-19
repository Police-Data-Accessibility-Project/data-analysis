from typing import Optional

from pydantic import BaseModel


class GetBagOfWordsOutcome(BaseModel):
    url: str
    bag_of_words: Optional[dict] = None
    error: Optional[str] = None

