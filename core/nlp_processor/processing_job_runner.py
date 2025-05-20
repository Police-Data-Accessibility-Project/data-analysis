from typing import List, Type, Tuple

from core.database_logic.database_client import DatabaseClient
from core.nlp_processor.dtos.batch_state import BatchState
from core.nlp_processor.processing_jobs.extract_url_component import ExtractURLDomain, ExtractURLSuffix, \
    ExtractURLFileFormat, ExtractURLScheme, ExtractURLSubdomain, ExtractURLPath, ExtractURLQueryParams, \
    ExtractURLFragment
from core.nlp_processor.processing_jobs.url_html_processing_job_base import URLHTMLProcessingJobBase

class ProcessingJobRunner:

    def __init__(
        self,
        db_client: DatabaseClient
    ):
        self.db_client = db_client

    async def run_all_for_url(self, state: BatchState):
        jobs = state.jobs
        entries: List[Tuple[JobInfo, Type[URLHTMLProcessingJobBase]]] = [
            (jobs.url_component_domain, ExtractURLDomain),
            (jobs.url_component_suffix, ExtractURLSuffix),
            (jobs.url_component_scheme, ExtractURLScheme),
            (jobs.url_component_path, ExtractURLPath),
            (jobs.url_component_subdomain, ExtractURLSubdomain),
            (jobs.url_component_fragment, ExtractURLFragment),
            (jobs.url_component_query_params, ExtractURLQueryParams),
            (jobs.url_component_file_format, ExtractURLFileFormat),
        ]
        for job_info, cls in entries:
            if not job_info.processed:
                job: URLHTMLProcessingJobBase = cls(
                    db_client=self.db_client,
                    context=state.context
                )
                job_info.value = await job.run()

    async def run_all(self):
        while True:
            batch = await self.db_client.get_next_valid_url_batch_for_nlp_preprocessing()
            if batch is None:
                break
            url_info = batch.context.url_info
            url_id = url_info.id
            print(f"Processing {url_id} {url_info.url}...")
            await self.run_all_for_url(batch)
            await self.db_client.upload_batch_jobs(
                url_id=url_id,
                jobs=batch.jobs
            )