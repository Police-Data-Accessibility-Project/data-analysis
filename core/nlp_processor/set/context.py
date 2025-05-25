from typing import Optional


from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, PrivateAttr
from spacy.tokens.doc import Doc

from core.db.dtos.output.url import URLOutput


class SetContext(BaseModel):
    """
    Represents a shared input for all jobs.

    All jobs might not use all fields,
    but these fields are all *available* to each job
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    url_info: URLOutput
    html: str
    _soup: Optional[BeautifulSoup] = PrivateAttr(default=None)
    _spacy_doc: Optional[Doc] = PrivateAttr(default=None)

    @property
    def soup(self) -> BeautifulSoup:
        if self._soup is None:
            self._soup = BeautifulSoup(self.html, "lxml")
        return self._soup

    @property
    def spacy_doc(self) -> Doc:
        if self._spacy_doc is None:
            from core.nlp_processor.globals import SPACY_MODEL
            text = self.soup.get_text(separator=' ', strip=True)
            self._spacy_doc = SPACY_MODEL(text)
        return self._spacy_doc
