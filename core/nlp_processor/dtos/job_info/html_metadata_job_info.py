from typing import Optional

from pydantic import BaseModel

from core.database_logic.enums import HTMLMetadataType
from core.nlp_processor.dtos.job_info.job_info import JobInfo


class HTMLMetadataInfo(BaseModel):
    type: HTMLMetadataType
    value: str

class HTMLMetadataJobInfo(JobInfo):
    value: Optional[HTMLMetadataInfo] = None