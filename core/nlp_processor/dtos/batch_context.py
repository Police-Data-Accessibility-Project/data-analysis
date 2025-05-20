from typing import Optional

from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, PrivateAttr

from core.database_logic.dtos.url_info import URLInfo


class BatchContext(BaseModel):
    """
    Represents a shared input for all jobs.

    All jobs might not use all fields,
    but these fields are all *available* to each job
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    url_info: URLInfo
    html: str
    _soup: Optional[BeautifulSoup] = PrivateAttr(default=None)

    @property
    def soup(self) -> BeautifulSoup:
        if self._soup is None:
            self._soup = BeautifulSoup(self.html, "lxml")
        return self._soup
