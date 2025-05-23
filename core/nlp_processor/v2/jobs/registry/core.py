from core.nlp_processor.v2.jobs.identifiers.job_identifier_base import JobIdentifierBase
from core.nlp_processor.v2.jobs.processors.job_processor_base import JobProcessorBase
from core.nlp_processor.v2.jobs.registry.entry import JobRegistryEntry


class JobRegistry:

    def __init__(self, registry_entries: list[JobRegistryEntry]):
        self._map: dict[JobIdentifierBase, type[JobProcessorBase]] = {}
        for entry in registry_entries:
            self._map[entry.identifier] = entry.processor

    def get_processor(self, identifier: JobIdentifierBase) -> type[JobProcessorBase]:
        return self._map[identifier]

    def get_identifiers(self) -> list[JobIdentifierBase]:
        return list(self._map.keys())