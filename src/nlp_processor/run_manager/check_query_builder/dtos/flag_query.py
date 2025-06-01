from typing import Any

from src.shared.bases.pydantic.arbitrary_base_model import ArbitraryBaseModel


class FlagQuery(ArbitraryBaseModel):
    cte: Any
    label: str
    select: Any
