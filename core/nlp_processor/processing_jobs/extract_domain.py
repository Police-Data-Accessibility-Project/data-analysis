from typing import Any

from core.nlp_processor.processing_jobs.url_html_processing_job_base import URLHTMLProcessingJobBase


class ExtractDomainJob(URLHTMLProcessingJobBase):

    @property
    def process_name(self):
        return 'extract_domain'

    async def download_additional_data(self):
        return None

    async def get_d

    async def process(self, data: Any):
