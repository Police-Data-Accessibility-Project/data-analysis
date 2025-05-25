import sys
from enum import Enum
from typing import List, Type, Optional

from core.db.client import DatabaseClient
from core.db.enums import ErrorType
from core.nlp_processor.set.context import SetContext
from core.nlp_processor.families.registry.instances import FAMILY_REGISTRY
from core.nlp_processor.jobs.registry.instances.all import JOB_REGISTRY
from core.nlp_processor.jobs.identifiers.base import JobIdentifierBase
from core.nlp_processor.jobs.result.base import JobResultBase
from core.nlp_processor.set.state import SetState
from core.utils.exception import format_exception
from loguru import logger

class HandleErrorType(Enum):
    RAISE = 1
    LOG = 2


class RunManager:

    def __init__(
        self,
        db_client: DatabaseClient,
        handle_error: HandleErrorType = HandleErrorType.RAISE
    ):
        self.db_client = db_client
        self.handle_error = handle_error

    async def run(
        self,
        available_job_ids: List[JobIdentifierBase]
    ):
        run_job_ids = await self.db_client.get_run_jobs(available_job_ids)
        if len(run_job_ids) == 0:
            logger.info("No jobs to run; exiting")
            return
        logger.info(f"Running set with {len(run_job_ids)} unique jobs")
        set_state = await self.db_client.get_next_url_set(run_job_ids)
        while set_state is not None:
            url_info = set_state.context.url_info
            logger.info(f"Running set on URL {url_info.id}: {url_info.url}")
            await self.run_for_set(set_state)
            set_state = await self.db_client.get_next_url_set(run_job_ids)

    async def run_for_set(self, set_state: SetState):
        job_results: List[JobResultBase] = []
        for job_id in set_state.job_ids:
            job_result = await self.run_for_job(
                job_id,
                context=set_state.context
            )
            if job_result is None:
                continue
            job_results.append(job_result)

        await self.db_client.upload_jobs_for_set(
            url_id=set_state.context.url_info.id,
            job_results=job_results
        )

    async def run_for_job(
        self,
        job_id: JobIdentifierBase,
        context: SetContext
    ) -> Optional[JobResultBase]:
        processor_class = JOB_REGISTRY.get_processor(job_id)
        processor = processor_class(context=context)
        try:
            job_result_class: Type[JobResultBase] = FAMILY_REGISTRY.get_job_result_class(
                job_id.family
            )
            return job_result_class(
                job_id=job_id,
                result=await processor.process()
            )

        except Exception as e:
            if self.handle_error == HandleErrorType.RAISE:
                raise

            msg = format_exception(e)
            msg = f"Job: {job_id.__name__}; Error: {msg}"
            logger.error(msg)
            await self.db_client.add_url_error(
                url_id=context.url_info.id,
                error=msg,
                error_type=ErrorType.PARSE
            )
            return None



