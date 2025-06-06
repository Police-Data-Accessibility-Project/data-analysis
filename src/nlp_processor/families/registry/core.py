from src.db.models.base import FamilyModel
from src.nlp_processor.families.enum import FamilyType
from src.nlp_processor.families.registry.entry import FamilyRegistryEntry
from src.nlp_processor.jobs.mapper.base import JobResultMapperBase
from src.nlp_processor.jobs.result.base import JobResultBase


class FamilyRegistry:

    def __init__(self, registry_entries: list[FamilyRegistryEntry]):
        self._model_map: dict[FamilyType, type[FamilyModel]] = {}
        self._job_result_map: dict[FamilyType, type[JobResultBase]] = {}
        self._mapper_map: dict[FamilyType, type[JobResultMapperBase]] = {}
        for entry in registry_entries:
            self._model_map[entry.family] = entry.model
            self._job_result_map[entry.family] = entry.job_result_class
            self._mapper_map[entry.family] = entry.mapper_class

    def get_model(self, family: FamilyType) -> type[FamilyModel]:
        return self._model_map[family]

    def get_job_result_class(self, family: FamilyType) -> type[JobResultBase]:
        return self._job_result_map[family]

    def get_mapper_class(self, family: FamilyType) -> type[JobResultMapperBase]:
        return self._mapper_map[family]