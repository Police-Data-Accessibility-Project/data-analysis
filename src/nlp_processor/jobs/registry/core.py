from src.nlp_processor.jobs.identifiers.base import JobIdentifierBase
from src.nlp_processor.jobs.processors.base import JobProcessorBase
from src.nlp_processor.jobs.registry.entry import JobRegistryEntry


class JobRegistry:

    def __init__(self, registry_entries: list[JobRegistryEntry]):
        self._map: dict[JobIdentifierBase, type[JobProcessorBase]] = {}
        for entry in registry_entries:
            self._map[entry.identifier] = entry.processor

    def get_processor(self, identifier: JobIdentifierBase) -> type[JobProcessorBase]:
        return self._map[identifier]

    def get_identifiers(self) -> list[JobIdentifierBase]:
        return list(self._map.keys())