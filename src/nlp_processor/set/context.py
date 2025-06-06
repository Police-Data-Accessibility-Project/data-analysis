from typing import Optional

from bs4 import BeautifulSoup
from pydantic import PrivateAttr
from spacy.tokens.doc import Doc

from src.db.dtos.output.url import URLOutput
from src.shared.bases.pydantic.arbitrary_base_model import ArbitraryBaseModel


class SetContext(ArbitraryBaseModel):
    """
    Represents a shared input for all jobs.

    All jobs might not use all fields,
    but these fields are all *available* to each job
    """
    url_info: URLOutput
    html: Optional[str]
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
            from src.nlp_processor.globals import SPACY_MODEL
            text = self.soup.get_text(separator=' ', strip=True)
            self._spacy_doc = SPACY_MODEL(text)
        return self._spacy_doc

    def unload(self):
        """Free up memory by discarding cached content."""
        self.html = None
        self._soup = None
        self._spacy_doc = None