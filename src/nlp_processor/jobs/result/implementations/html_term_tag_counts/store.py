from collections import Counter, defaultdict

Term = str
Tag = str
Store = dict[Term, dict[Tag, int]]

class TermTagStore:

    def __init__(self):
        self._dict: Store = defaultdict(Counter)

    def add(self, term: Term, tag: Tag):
        self._dict[term][tag] += 1

    def get(self, term: Term, tag: Tag) -> int:
        return self._dict[term][tag]

    def get_all_terms(self) -> list[Term]:
        return list(self._dict.keys())

    def get_tags_for_term(self, term: Term) -> list[Tag]:
        return list(self._dict[term].keys())

    def get_all_tags(self) -> list[Tag]:
        return list(
            {
                tag for tags in self._dict.values()
                for tag in tags.keys()
            }
        )

