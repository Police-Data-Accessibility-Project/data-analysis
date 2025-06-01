from src.db.models.core import HTMLMetadata, URLComponent, HTMLContentMetric, HTMLBagOfWords, HTMLTermTagCount, \
        HTMLBagOfTags
from src.nlp_processor.families.enum import FamilyType
from src.nlp_processor.families.registry.core import FamilyRegistry
from src.nlp_processor.families.registry.entry import FamilyRegistryEntry
from src.nlp_processor.jobs.mapper.direct.implementations import HTMLMetadataMapper, URLComponentMapper, \
        HTMLContentMetricMapper
from src.nlp_processor.jobs.mapper.lookup.implementations.html_bag_of_tags import HTMLBagOfTagsMapper
from src.nlp_processor.jobs.mapper.lookup.implementations.html_bag_of_words import HTMLBagOfWordsMapper
from src.nlp_processor.jobs.mapper.lookup.implementations.html_term_tag_counts import HTMLTermTagCountsMapper
from src.nlp_processor.jobs.result.implementations.html_bag_of_tags.core import HTMLBagOfTagsJobResult
from src.nlp_processor.jobs.result.implementations.html_bag_of_words.core import HTMLBagOfWordsJobResult
from src.nlp_processor.jobs.result.implementations.html_content_metric.core import HTMLContentMetricJobResult
from src.nlp_processor.jobs.result.implementations.html_metadata.core import HTMLMetadataJobResult
from src.nlp_processor.jobs.result.implementations.html_term_tag_counts.core import HTMLTermTagCountJobResult

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
        ),
        FamilyRegistryEntry(
            family=FamilyType.HTML_BAG_OF_TAGS,
            model=HTMLBagOfTags,
            job_result_class=HTMLBagOfTagsJobResult,
            mapper_class=HTMLBagOfTagsMapper
        )
    ]
)
