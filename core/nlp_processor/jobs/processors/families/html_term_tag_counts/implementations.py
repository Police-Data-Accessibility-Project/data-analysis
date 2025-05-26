import gc

from core.nlp_processor.globals import SPACY_MODEL
from core.nlp_processor.jobs.processors.base import JobProcessorBase
from core.nlp_processor.jobs.result.implementations.html_term_tag_counts.store import TermTagStore



class HTMLTermTagCountsProcessor(JobProcessorBase):
    GARBAGE_COLLECT_INTERVAL = 500
    EXCLUDED_TAGS = {
        'script',
        'style',
        'link',
        'html',
    }


    async def process(self) -> TermTagStore:
        store = TermTagStore()
        soup = self.soup
        for idx, tag in enumerate(soup.find_all(True)):
            if tag.name is None:
                continue
            tag_name = str(tag.name).lower()
            if tag_name in self.EXCLUDED_TAGS:
                continue
            text = tag.get_text(separator=' ', strip=True)
            if not text:
                continue

            doc = SPACY_MODEL(text)

            for token in doc:
                if not token.is_alpha:
                    continue
                if not token.is_stop:
                    continue

                term = token.lemma_.lower()
                store.add(term, tag_name)

            # Delete and occasionally garbage collect to keep memory usage down
            del doc
            if idx % self.GARBAGE_COLLECT_INTERVAL == 0:
                gc.collect()

        return store