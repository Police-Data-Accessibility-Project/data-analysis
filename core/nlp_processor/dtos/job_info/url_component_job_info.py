from typing import Optional

from pydantic import BaseModel

from core.database_logic.enums import ComponentType
from core.nlp_processor.dtos.job_info.job_info import JobInfo


class ComponentInfo(BaseModel):
    type: ComponentType
    value: str


class URLComponentJobInfo(JobInfo):
    value: Optional[ComponentInfo] = None