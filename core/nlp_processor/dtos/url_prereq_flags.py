from pydantic import BaseModel


class URLPrereqFlags(BaseModel):
    """
    A set of booleans for all processing prerequisite flags
    """
    url_component_scheme: bool
    url_component_domain: bool
    url_component_subdomain: bool
    url_component_path: bool
    url_component_fragment: bool
    url_component_query_params: bool
    url_component_file_format: bool
    url_component_suffix: bool