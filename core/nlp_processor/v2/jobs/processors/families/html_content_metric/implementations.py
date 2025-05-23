from core.nlp_processor.v2.jobs.processors.families.html_content_metric._template import \
    ExtractHTMLContentMetricProcessorTemplate
from core.nlp_processor.v2.jobs.processors.families.html_content_metric.factory import \
    make_html_content_metric_link_direction_processor
from core.nlp_processor.v2.jobs.enums import HTMLContentMetricJobType



class ExtractHTMLContentMetricsEmailProcessor(ExtractHTMLContentMetricProcessorTemplate):

    async def process(self) -> int:
        a_tags = self.soup.find_all("a", href=True)
        mailto_links = {
            a["href"][7:] for a in a_tags if a["href"].startswith("mailto:")
        }
        text_emails = {token.text for token in self.spacy_doc if token.like_email}
        
        return len(
            mailto_links.union(text_emails)
        )


ExtractHTMLContentMetricsInternalLinkProcessor = make_html_content_metric_link_direction_processor(
    metric_type=HTMLContentMetricJobType.INTERNAL_LINKS,
    is_external=False
)

ExtractHTMLContentMetricsExternalLinkProcessor = make_html_content_metric_link_direction_processor(
    metric_type=HTMLContentMetricJobType.EXTERNAL_LINKS,
    is_external=True
)