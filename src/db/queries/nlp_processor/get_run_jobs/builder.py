from sqlalchemy import select

from src.db.queries.builder import QueryBuilderBase
from src.nlp_processor.jobs.identifiers.base import JobIdentifierBase
from src.nlp_processor.run_manager.check_query_builder.core import CheckQueryBuilder


class GetRunJobsQueryBuilder(QueryBuilderBase):

    def __init__(self, job_ids: list[JobIdentifierBase]):
        super().__init__()
        self.job_ids = job_ids


    async def run(self) -> list[JobIdentifierBase]:
        builder = CheckQueryBuilder(self.job_ids)
        subqs = []
        for job_id in builder.job_ids:
            subq = builder.build_global_subquery(job_id)
            subqs.append(subq)
        query = select(*subqs)

        execution_result = await self._session.execute(query)
        row = execution_result.mappings().one_or_none()

        missing_jobs = []
        for label in builder.get_all_labels():
            any_url_missing_job = row[label]
            if any_url_missing_job:
                job_id = builder.get_job_id_from_label(label)
                missing_jobs.append(job_id)

        return missing_jobs

