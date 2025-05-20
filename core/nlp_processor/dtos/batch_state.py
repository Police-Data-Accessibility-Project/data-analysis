from pydantic import BaseModel

from core.nlp_processor.dtos.batch_context import BatchContext
from core.nlp_processor.dtos.batch_jobs import BatchJobs


class BatchState(BaseModel):
    context: BatchContext
    jobs: BatchJobs