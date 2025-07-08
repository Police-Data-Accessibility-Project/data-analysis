from sqlalchemy import select, or_

from src.db.dtos.output.url import URLOutput
from src.db.models.core import URLCompressedHTML, URL
from src.db.queries.builder import QueryBuilderBase
from src.nlp_processor.jobs.identifiers.base import JobIdentifierBase
from src.nlp_processor.run_manager.check_query_builder.core import CheckQueryBuilder
from src.nlp_processor.set.context import SetContext
from src.nlp_processor.set.state import SetState


class GetAllURLSetsQueryBuilder(QueryBuilderBase):

    def __init__(self, job_ids: list[JobIdentifierBase]):
        super().__init__()
        self.job_ids = job_ids

    async def run(self) -> list[SetState] | None:
        if len(self.job_ids) == 0:
            return None
        builder = CheckQueryBuilder(self.job_ids)
        sqs = builder.get_flag_select_subqueries()
        select_statements = [sq.select for sq in sqs]
        query = select(
            URL.id,
            URL.url,
            *select_statements,
        ).join(
            URLCompressedHTML
        )

        # Outer join for every family with jobs present
        query = builder.add_cte_outer_joins(query, sqs)

        query = query.where(
            or_(
                *select_statements
            )
        )

        execution_result = await self._session.execute(query)
        row = execution_result.mappings().all()

        set_states = []
        for row in row:
            set_jobs = []
            for label in builder.get_all_labels():
                url_missing_job = row[label]
                if url_missing_job:
                    job_id = builder.get_job_id_from_label(label)
                    set_jobs.append(job_id)

            set_states.append(
                SetState(
                    context=SetContext(
                        url_info=URLOutput(
                            id=row["id"],
                            url=row["url"],
                        ),
                        html=None,
                    ),
                    job_ids=set_jobs
                )
            )
        return set_states
