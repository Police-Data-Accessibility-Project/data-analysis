from pydantic import BaseModel

from core.database_logic.dtos.url_info import URLInfo


class URLHTMLProcessingJobInfo(BaseModel):
    url_info: URLInfo
    html: str
