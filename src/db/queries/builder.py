from abc import abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class QueryBuilderBase:


    def __init__(self):
        self._session: AsyncSession | None = None

    @abstractmethod
    async def run(self) -> Any:
        raise NotImplementedError

    async def execute_scalar(self, query: Any) -> Any:
        result = await self._session.execute(query)
        return result.scalar()

    async def execute_all(self, query: Any) -> Any:
        result = await self._session.execute(query)
        return result.all()

    async def build(self, session: AsyncSession) -> Any:
        self._session = session
        return self.run()