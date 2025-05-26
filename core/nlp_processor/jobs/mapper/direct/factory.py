from core.db.models.core import FamilyModel
from core.nlp_processor.jobs.mapper.direct.base import DirectJobResultMapperBase
from core.nlp_processor.jobs.result.base import JobResultBase

def get_type_value_mapper(model: type[FamilyModel]) -> type[DirectJobResultMapperBase]:

    class TypeValueMapper(DirectJobResultMapperBase):

        async def map(
            self,
            job_result: JobResultBase,
            url_id: int
        ) -> list[FamilyModel]:
            return [model(
                url_id=url_id,
                type=job_result.job_id.job_type.value,
                value=job_result.result
            )]

    TypeValueMapper.__name__ = f"{model.__name__}JobMapper"

    return TypeValueMapper