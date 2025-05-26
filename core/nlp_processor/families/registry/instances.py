from core.db.models.core import HTMLMetadata, URLComponent, HTMLContentMetric, HTMLBagOfWords, HTMLTermTagCount
from core.nlp_processor.families.enum import FamilyType
from core.nlp_processor.families.registry.core import FamilyRegistry
from core.nlp_processor.families.registry.entry import FamilyRegistryEntry
from core.nlp_processor.jobs.mapper.direct.implementations import HTMLMetadataMapper, URLComponentMapper, \
        HTMLContentMetricMapper, HTMLBagOfWordsMapper
from core.nlp_processor.jobs.mapper.lookup.implementations import HTMLTermTagCountsMapper
from core.nlp_processor.jobs.result.implementations.html_bag_of_words.core import HTMLBagOfWordsJobResult
from core.nlp_processor.jobs.result.implementations.html_content_metric.core import HTMLContentMetricJobResult
from core.nlp_processor.jobs.result.implementations.html_metadata.core import HTMLMetadataJobResult
from core.nlp_processor.jobs.result.implementations.html_term_tag_counts.core import HTMLTermTagCountJobResult

FAMILY_REGISTRY = FamilyRegistry(
    [
        FamilyRegistryEntry(
            family=FamilyType.HTML_METADATA,
            model=HTMLMetadata,
            job_result_class=HTMLMetadataJobResult,
            mapper_class=HTMLMetadataMapper
        ),
        FamilyRegistryEntry(
            family=FamilyType.URL_COMPONENT,
            model=URLComponent,
            job_result_class=HTMLMetadataJobResult,
            mapper_class=URLComponentMapper
        ),
        FamilyRegistryEntry(
            family=FamilyType.HTML_CONTENT_METRIC,
            model=HTMLContentMetric,
            job_result_class=HTMLContentMetricJobResult,
            mapper_class=HTMLContentMetricMapper
        ),
        FamilyRegistryEntry(
            family=FamilyType.HTML_BAG_OF_WORDS,
            model=HTMLBagOfWords,
            job_result_class=HTMLBagOfWordsJobResult,
            mapper_class=HTMLBagOfWordsMapper
        ),
        FamilyRegistryEntry(
            family=FamilyType.HTML_TERM_TAG_COUNTS,
            model=HTMLTermTagCount,
            job_result_class=HTMLTermTagCountJobResult,
            mapper_class=HTMLTermTagCountsMapper
        )
    ]
)
