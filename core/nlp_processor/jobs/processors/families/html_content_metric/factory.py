from tldextract import extract

from core.nlp_processor.jobs.processors.families.html_content_metric._template import \
    ExtractHTMLContentMetricProcessorTemplate
from core.nlp_processor.jobs.enums import HTMLContentMetricJobType

def make_html_content_metric_link_direction_processor(
    metric_type: HTMLContentMetricJobType,
    is_external: bool
):

    class ExtractHTMLMetricLinkProcessor(ExtractHTMLContentMetricProcessorTemplate):

        def is_external_link(self, url: str) -> bool:
            base_domain = extract(self.url).domain
            other_domain = extract(url).domain
            return base_domain != other_domain


        async def process(self) -> int:
            anchor_urls = {a['href'] for a in self.soup.find_all("a", href=True)}
            text_urls = {token.text for token in self.spacy_doc if token.like_url}
            all_urls = anchor_urls.union(text_urls)

            count = 0
            for url in all_urls:
                if self.is_external_link(url) == is_external:
                    count += 1

            return count

    title = metric_type.name.title().replace('_', '')
    ExtractHTMLMetricLinkProcessor.__name__ = (
        f"ExtractHTML{title}MetricProcessor"
    )
    return ExtractHTMLMetricLinkProcessor