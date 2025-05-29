from core.db.models.core import HTMLMetadata, URLComponent, HTMLContentMetric
from core.nlp_processor.jobs.mapper.direct.factory import get_type_value_mapper

HTMLMetadataMapper = get_type_value_mapper(HTMLMetadata)

URLComponentMapper = get_type_value_mapper(URLComponent)

HTMLContentMetricMapper = get_type_value_mapper(HTMLContentMetric)
