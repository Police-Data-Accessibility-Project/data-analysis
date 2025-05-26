from abc import ABC, abstractmethod

from core.db.models.core import FamilyModel


class JobResultMapperBase(ABC):

    @abstractmethod
    async def map(
        self,
        *args,
        **kwargs
    ) -> list[FamilyModel]:
        ...