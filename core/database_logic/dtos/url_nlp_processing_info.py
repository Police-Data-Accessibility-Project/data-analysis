from pydantic import BaseModel

from core.nlp_processor.dtos.url_prereq_flags import URLPrereqFlags
from core.nlp_processor.dtos.url_html_processing_job_info import URLHTMLProcessingJobInfo


class URLNLPProcessingInfo(BaseModel):
    job_info: URLHTMLProcessingJobInfo
    prereq_flags: URLPrereqFlags
