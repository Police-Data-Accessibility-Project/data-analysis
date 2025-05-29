from typing import Any

from pydantic import BaseModel, ConfigDict


class FlagQuery(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cte: Any
    label: str
    select: Any
