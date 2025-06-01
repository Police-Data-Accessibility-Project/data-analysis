from typing import Any

from sqlalchemy import func, exists, and_, select

from src.db.models.core import URL, URLCompressedHTML
from src.nlp_processor.run_manager.check_query_builder.dtos.flag_query import FlagQuery
from src.nlp_processor.families.registry.instances import FAMILY_REGISTRY
from src.nlp_processor.jobs.identifiers.base import JobIdentifierBase


class CheckQueryBuilder:

    def __init__(self, job_ids: list[JobIdentifierBase]):
        self.job_ids = job_ids
        self.label_id_lookup = {
            self.get_label(job_id): job_id for job_id in self.job_ids
        }

    def get_all_labels(self) -> list[str]:
        return list(self.label_id_lookup.keys())

    def get_job_id_from_label(self, label: str) -> JobIdentifierBase:
        return self.label_id_lookup[label]

    def build_global_subquery(
        self,
        job_id: JobIdentifierBase,
    ) -> Any:
        """
        Checks if ANY URL is missing the given job
        :param job_id:
        :return:
        """
        model = FAMILY_REGISTRY.get_model(job_id.family)
        job_type = job_id.job_type
        label = self.get_label(job_id)

        return exists(
            select(URL.id)
            .join(URLCompressedHTML)
            .where(
                ~exists(
                    select(model.id)
                    .where(
                        and_(
                            model.url_id == URL.id,
                            model.type == job_type.value
                        )
                    )
                )
            )
        ).label(label)

    def get_flag_select_subqueries(self) -> list[FlagQuery]:
        sqs = []
        for job_id in self.job_ids:
            cte = self.build_flag_cte(job_id)
            label = self.get_label(job_id)
            select = func.coalesce(
                cte.c[label], True
            ).label(label)
            sqs.append(
                FlagQuery(
                    cte=cte,
                    label=label,
                    select=select
                )
            )
        return sqs

    def add_cte_outer_joins(self, query, sqs: list[FlagQuery]):
        for sq in sqs:
            cte = sq.cte
            query = query.outerjoin(
                cte,
                cte.c.url_id == URL.id
            )
        return query

    def build_flag_cte(
        self,
        job_id: JobIdentifierBase,
    ) -> Any:
        model = FAMILY_REGISTRY.get_model(job_id.family)
        job_type = job_id.job_type
        label = self.get_label(job_id)
        return select(
            model.url_id,
            ~func.bool_or(
                model.type == job_type.value
            ).label(label)
        ).group_by(model.url_id).cte(label)



    @staticmethod
    def get_label(job_id: JobIdentifierBase) -> str:
        family = job_id.family
        return f"missing_{family.value}_{job_id.job_type.value}"

