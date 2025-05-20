from pydantic import BaseModel

from core.nlp_processor.dtos.job_info.html_metadata_job_info import HTMLMetadataJobInfo
from core.nlp_processor.dtos.job_info.url_component_job_info import URLComponentJobInfo


class BatchJobs(BaseModel):
    url_component_scheme: URLComponentJobInfo
    url_component_domain: URLComponentJobInfo
    url_component_subdomain: URLComponentJobInfo
    url_component_path: URLComponentJobInfo
    url_component_fragment: URLComponentJobInfo
    url_component_query_params: URLComponentJobInfo
    url_component_file_format: URLComponentJobInfo
    url_component_suffix: URLComponentJobInfo
    html_metadata_title: HTMLMetadataJobInfo
    html_metadata_description: HTMLMetadataJobInfo
    html_metadata_keywords: HTMLMetadataJobInfo
    html_metadata_author: HTMLMetadataJobInfo

    @staticmethod
    def initialize_with_processed_flags(
        url_component_scheme: bool,
        url_component_domain: bool,
        url_component_subdomain: bool,
        url_component_path: bool,
        url_component_fragment: bool,
        url_component_query_params: bool,
        url_component_file_format: bool,
        url_component_suffix: bool,
        html_metadata_title: bool,
        html_metadata_description: bool,
        html_metadata_keywords: bool,
        html_metadata_author: bool
    ) -> 'BatchJobs':
        return BatchJobs(
            url_component_scheme=URLComponentJobInfo(processed=url_component_scheme),
            url_component_domain=URLComponentJobInfo(processed=url_component_domain),
            url_component_subdomain=URLComponentJobInfo(processed=url_component_subdomain),
            url_component_path=URLComponentJobInfo(processed=url_component_path),
            url_component_fragment=URLComponentJobInfo(processed=url_component_fragment),
            url_component_query_params=URLComponentJobInfo(processed=url_component_query_params),
            url_component_file_format=URLComponentJobInfo(processed=url_component_file_format),
            url_component_suffix=URLComponentJobInfo(processed=url_component_suffix),
            html_metadata_title=HTMLMetadataJobInfo(processed=html_metadata_title),
            html_metadata_description=HTMLMetadataJobInfo(processed=html_metadata_description),
            html_metadata_keywords=HTMLMetadataJobInfo(processed=html_metadata_keywords),
            html_metadata_author=HTMLMetadataJobInfo(processed=html_metadata_author),
        )