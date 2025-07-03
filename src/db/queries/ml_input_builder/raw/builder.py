from sqlalchemy import select

from src.db.format import rows_to_list_of_simple_dicts
from src.db.models.core import URL, URLAnnotations, URLCompressedHTML
from src.db.queries.builder import QueryBuilderBase

import polars as pl

from src.utils.compression import decompress_html


class RawMLInputQueryBuilder(QueryBuilderBase):

    async def run(self) -> pl.DataFrame:

        query = (
            select(
                URL.url,
                URLAnnotations.relevant,
                URLAnnotations.record_type_fine,
                URLAnnotations.record_type_coarse,
                URLCompressedHTML.compressed_html
            )
            .outerjoin(URLAnnotations, URLAnnotations.url_id == URL.id)
            .outerjoin(URLCompressedHTML, URLCompressedHTML.url_id == URL.id)
        )

        raw_results = await self.execute_all(query)
        results = []
        for raw_result in raw_results:
            d = {
                "url": raw_result[0],
                "relevant": raw_result[1],
                "record_type_fine": raw_result[2].value if raw_result[2] is not None else None,
                "record_type_coarse": raw_result[3].value if raw_result[3] is not None else None,
                "html": decompress_html(raw_result[4]) if raw_result[4] is not None else None
            }
            results.append(d)

        return pl.DataFrame(results)