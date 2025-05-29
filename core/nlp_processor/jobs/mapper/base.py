from abc import ABC, abstractmethod

from core.db.models.base import FamilyModel


class JobResultMapperBase(ABC):

    @abstractmethod
    async def map(
        self,
        *args,
        **kwargs
    ) -> list[FamilyModel]:
        ...