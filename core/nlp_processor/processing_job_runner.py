from typing import List, Type, Tuple

from core.database_logic.database_client import DatabaseClient
from core.database_logic.dtos.url_nlp_processing_info import URLNLPProcessingInfo
from core.nlp_processor.processing_jobs.extract_url_component_base import ExtractURLDomain, ExtractURLSuffix, \
    ExtractURLFileFormat, ExtractURLScheme, ExtractURLSubdomain, ExtractURLPath, ExtractURLQueryParams, \
    ExtractURLFragment
from core.nlp_processor.processing_jobs.url_html_processing_job_base import URLHTMLProcessingJobBase

class ProcessingJobRunner:

    def __init__(
        self,
        db_client: DatabaseClient
    ):
        self.db_client = db_client

    async def run_all_for_url(self, pi: URLNLPProcessingInfo):
        pf = pi.prereq_flags
        entries: List[Tuple[bool, Type[URLHTMLProcessingJobBase]]] = [
            (pf.url_component_domain, ExtractURLDomain),
            (pf.url_component_suffix, ExtractURLSuffix),
            (pf.url_component_scheme, ExtractURLScheme),
            (pf.url_component_path, ExtractURLPath),
            (pf.url_component_subdomain, ExtractURLSubdomain),
            (pf.url_component_fragment, ExtractURLFragment),
            (pf.url_component_query_params, ExtractURLQueryParams),
            (pf.url_component_file_format, ExtractURLFileFormat),
        ]
        for flag, cls in entries:
            if not flag:
                job: URLHTMLProcessingJobBase = cls(
                    db_client=self.db_client,
                    job_info=pi.job_info
                )
                await job.run()

    async def run_all(self):
        while True:
            pi = await self.db_client.get_next_valid_url_for_nlp_preprocessing()
            if pi is None:
                break
            print(f"Processing {pi.job_info.url_info.id} {pi.job_info.url_info.url}...")
            await self.run_all_for_url(pi)