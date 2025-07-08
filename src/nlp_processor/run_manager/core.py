from typing import List, Type, Optional

import tqdm
from loguru import logger

from src.db.client import DatabaseClient
from src.db.enums import ErrorType
from src.nlp_processor.families.registry.instances import FAMILY_REGISTRY
from src.nlp_processor.jobs.identifiers.base import JobIdentifierBase
from src.nlp_processor.jobs.registry.instances.all import JOB_REGISTRY
from src.nlp_processor.jobs.result.base import JobResultBase
from src.nlp_processor.run_manager.enums import HandleErrorType
from src.nlp_processor.set.context import SetContext
from src.nlp_processor.set.state import SetState
from src.utils.exception import format_exception


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
        run_job_ids = await self.db_client.get_run_jobs(job_ids=available_job_ids)
        if len(run_job_ids) == 0:
            logger.info("No jobs to run; exiting")
            return
        logger.info(f"Running set with {len(run_job_ids)} unique jobs")
        logger.info(f"Jobs: {[j.job_type.value for j in run_job_ids]}")
        run_sets = await self.db_client.get_all_url_sets(run_job_ids)
        run_count = len(run_sets)
        if run_count == 0:
            logger.info("No URLs to process; exiting")
            return
        logger.info(f"Run count: {run_count}")
        with tqdm.trange(run_count) as t:
            for i in t:
                set_state = run_sets[i]
                url_info = set_state.context.url_info
                t.set_description(f"URL {url_info.id}")
                set_state.context.html = await self.db_client.get_html_for_url(
                    url_id=url_info.id
                )
                await self.run_for_set(set_state)
                set_state.context.unload()

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



