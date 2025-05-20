from typing import Optional, Any

from pydantic import BaseModel



class JobInfo(BaseModel):
    """
    Generic Job Info.
    Also used for subclasses
    """

    processed: bool
    value: Optional[Any] = None
