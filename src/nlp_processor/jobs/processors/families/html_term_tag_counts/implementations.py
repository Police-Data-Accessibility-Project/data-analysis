from bs4 import Tag

from src.nlp_processor.globals import SPACY_MODEL
from src.nlp_processor.jobs.processors.base import JobProcessorBase
from src.nlp_processor.jobs.result.implementations.html_term_tag_counts.store import TermTagStore


class HTMLTermTagCountsProcessor(JobProcessorBase):
    EXCLUDED_TAGS = [
        "html",
        "script",
        "link",
        "head",
        "meta",
        "style",
    ]

    @staticmethod
    def get_direct_text(tag: Tag) -> str:
        return " ".join(
            t.strip() for t in tag.find_all(string=True, recursive=False) if t.strip()
        )


    async def process(self) -> TermTagStore:
        store = TermTagStore()
        soup = self.soup

        texts_to_process = []
        tag_paths = []

        for tag in soup.find_all(True):
            tag_name = tag.name
            if not tag_name:
                continue
            tag_name = tag_name.lower()
            if tag_name in self.EXCLUDED_TAGS:
                continue

            direct_text = self.get_direct_text(tag)
            if not direct_text:
                continue

            texts_to_process.append(direct_text)
            # Add tag and its parents
            tag_paths.append(
                [
                    t.name.lower()
                    for t in [tag] + list(tag.parents)
                    if t.name is not None
                ]
            )

        for doc, tag_path in zip(SPACY_MODEL.pipe(texts_to_process, batch_size=32), tag_paths):
            for token in doc:
                if not token.is_alpha or token.is_stop:
                    continue
                lemma = token.lemma_.lower()
                for tag_name in tag_path:
                    if tag_name in self.EXCLUDED_TAGS:
                        continue
                    store.add(lemma, tag_name)

        return store