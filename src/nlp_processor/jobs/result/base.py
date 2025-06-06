from abc import ABC
from typing import Any

from pydantic import BaseModel

from src.nlp_processor.jobs.identifiers.base import JobIdentifierBase


class JobResultBase(BaseModel, ABC):
    job_id: JobIdentifierBase
    result: Any
