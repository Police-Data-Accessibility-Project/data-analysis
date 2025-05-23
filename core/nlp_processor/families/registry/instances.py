from core.db.models import HTMLMetadata, URLComponent, HTMLContentMetric, HTMLBagOfWords
from core.nlp_processor.families.enum import FamilyType
from core.nlp_processor.families.registry.core import FamilyRegistry
from core.nlp_processor.families.registry.entry import FamilyRegistryEntry
from core.nlp_processor.jobs.result.implementations import HTMLMetadataJobResult, URLComponentJobResult, \
        HTMLContentMetricJobResult, HTMLBagOfWordsJobResult

FAMILY_REGISTRY = FamilyRegistry(
    [
        FamilyRegistryEntry(
            family=FamilyType.HTML_METADATA,
            model=HTMLMetadata,
            job_result_class=HTMLMetadataJobResult
        ),
        FamilyRegistryEntry(
            family=FamilyType.URL_COMPONENT,
            model=URLComponent,
            job_result_class=URLComponentJobResult
        ),
        FamilyRegistryEntry(
            family=FamilyType.HTML_CONTENT_METRIC,
            model=HTMLContentMetric,
            job_result_class=HTMLContentMetricJobResult
        ),
        FamilyRegistryEntry(
            family=FamilyType.HTML_BAG_OF_WORDS,
            model=HTMLBagOfWords,
            job_result_class=HTMLBagOfWordsJobResult
        )
    ]
)
