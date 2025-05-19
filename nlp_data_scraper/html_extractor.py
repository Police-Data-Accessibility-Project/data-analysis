from collections import defaultdict
from typing import Optional, Dict, Counter

from bs4 import BeautifulSoup

from nlp_data_scraper.dtos.page_info import PageInfo


class HTMLExtractor:

    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_title(self) -> Optional[str]:
        if not self.soup.title:
            return None
        if not self.soup.title.string:
            return None
        return self.soup.title.string.strip()

    def get_meta_content(self, name: str) -> Optional[str]:
        tag = self.soup.find("meta", attrs={"name": name})
        if not tag:
            return None
        if not tag.get("content"):
            return None
        return tag["content"].strip()

    def get_description(self) -> Optional[str]:
        return self.get_meta_content("description")

    def get_keywords(self) -> Optional[str]:
        return self.get_meta_content("keywords")

    def get_all_text(self) -> str:
        return self.soup.get_text(separator=' ', strip=True)

    def get_link_text(self) -> str:
        link_texts = [
            a.get_text(separator=' ', strip=True)
            for a in self.soup.find_all('a')
            if a.get_text(strip=True)
        ]
        link_text = ' '.join(link_texts)
        return link_text

    def get_header_texts(self) -> Dict[str, str]:
        headers = defaultdict(list)
        for level in range(1, 7):
            tag = f'h{level}'
            headers[tag] = [
                h.get_text(separator=' ', strip=True)
                for h in self.soup.find_all(tag)
                if h.get_text(strip=True)
            ]
            headers[tag] = ' '.join(headers[tag])

        return headers

    def get_non_link_non_header_text(self) -> str:
        permitted_elements = [
            'a', 'img', 'p', 'span', 'div', 'li', 'ul', 'ol', 'table', 'tr', 'td', 'th', 'form', 'input', 'button', 'meta'
        ]

        non_link_non_header_text = [
            element.get_text(separator=' ', strip=True)
            for element in self.soup.find_all(permitted_elements)
            if element.get_text(strip=True)
        ]
        non_link_non_header_text = ' '.join(non_link_non_header_text)
        return non_link_non_header_text

    def get_tag_counts(self) -> Dict[str, int]:
        tag_counts = dict(Counter(tag.name for tag in self.soup.find_all(True)))
        return tag_counts

    def get_page_info(self) -> PageInfo:
        return PageInfo(
            title=self.get_title(),
            description=self.get_description(),
            keywords=self.get_keywords(),
            all_text=self.get_all_text(),
            link_text=self.get_link_text(),
            header_texts=self.get_header_texts(),
            non_link_non_header_text=self.get_non_link_non_header_text(),
            tag_counts=self.get_tag_counts(),
        )


def extract_html(text: str) -> PageInfo:
    extractor = HTMLExtractor(text)
    return extractor.get_page_info()