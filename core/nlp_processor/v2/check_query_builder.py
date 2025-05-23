from typing import Type, Any

from sqlalchemy import func, case, exists, not_, and_

from core.database_logic.models import URL
from core.nlp_processor.v2.families.registry.instances import FAMILY_REGISTRY
from core.nlp_processor.v2.jobs.identifiers.job_identifier_base import JobIdentifierBase


class CheckQueryBuilder:

    def __init__(self, job_ids: list[Type[JobIdentifierBase]]):
        self.job_ids = job_ids
        self.label_id_lookup = {
            self.get_label(job_id): job_id for job_id in self.job_ids
        }

    def get_all_labels(self) -> list[str]:
        return list(self.label_id_lookup.keys())

    def get_job_id_from_label(self, label: str) -> Type[JobIdentifierBase]:
        return self.label_id_lookup[label]


    def build_global_subquery(
        self,
        job_id: Type[JobIdentifierBase],
    ) -> Any:
        """
        Checks if ANY URL is missing the given job
        :param job_id:
        :return:
        """
        model = FAMILY_REGISTRY.get_model(job_id.family)
        job_type = job_id.job_type
        label = self.get_label(job_id)

        return ~exists().where(
                    and_(
                        model.url_id == URL.id,
                        model.type == job_type.value
                    )
                ).label(label)

    def get_flag_select_subqueries(self) -> list[Any]:
        subqueries = []
        for job_id in self.job_ids:
            subqueries.append(self.build_flag_subquery(job_id))
        return subqueries

    def add_family_outer_joins(self, query):
        family_set = set()
        for job_id in self.job_ids:
            family_set.add(job_id.family)
        for family in family_set:
            model = FAMILY_REGISTRY.get_model(family)
            query = query.outerjoin(model)
        return query


    def build_flag_subquery(
        self,
        job_id: Type[JobIdentifierBase],
    ) -> Any:
        model = FAMILY_REGISTRY.get_model(job_id.family)
        job_type = job_id.job_type
        return func.bool_or(
            case(
                (model.type == job_type.value, False),
                else_=True
            )
        ).label(self.get_label(job_id))


    @staticmethod
    def get_label(job_id: Type[JobIdentifierBase]) -> str:
        family = job_id.family
        return f"missing_{family.value}_{job_id.job_type.value}"

