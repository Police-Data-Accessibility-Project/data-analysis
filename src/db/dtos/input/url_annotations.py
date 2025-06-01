from pydantic import BaseModel

from src.db.enums import RecordTypeCoarse, RecordTypeFine


class URLAnnotationsInput(BaseModel):
    url: str
    relevant: bool
    record_type_fine: RecordTypeFine
    record_type_coarse: RecordTypeCoarse
