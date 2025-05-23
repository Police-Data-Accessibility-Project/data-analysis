from core.database_logic.models import FamilyModel
from core.nlp_processor.v2.families.enums import FamilyType
from core.nlp_processor.v2.families.registry.entry import FamilyRegistryEntry
from core.nlp_processor.v2.jobs.result.job_result_base import JobResultBase


class FamilyRegistry:

    def __init__(self, registry_entries: list[FamilyRegistryEntry]):
        self._model_map: dict[FamilyType, type[FamilyModel]] = {}
        self._job_result_map: dict[FamilyType, type[JobResultBase]] = {}
        for entry in registry_entries:
            self._model_map[entry.family] = entry.model
            self._job_result_map[entry.family] = entry.job_result_class

    def get_model(self, family: FamilyType) -> type[FamilyModel]:
        return self._model_map[family]

    def get_job_result_class(self, family: FamilyType) -> type[JobResultBase]:
        return self._job_result_map[family]