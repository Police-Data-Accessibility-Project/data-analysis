from pydantic import BaseModel

from core.nlp_processor.dtos.batch_context import SetContext
from core.nlp_processor.dtos.batch_jobs import BatchJobs


class BatchState(BaseModel):
    context: SetContext
    jobs: BatchJobs