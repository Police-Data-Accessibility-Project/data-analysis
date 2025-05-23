from typing import Optional

from pydantic import BaseModel

from core.database_logic.enums import HTMLContentMetricType
from core.nlp_processor.dtos.job_info.job_info import JobInfo


class HTMLContentMetricInfo(BaseModel):
    type: HTMLContentMetricType
    value: int

class HTMLMetadataJobInfo(JobInfo):
    value: Optional[HTMLContentMetricInfo] = None