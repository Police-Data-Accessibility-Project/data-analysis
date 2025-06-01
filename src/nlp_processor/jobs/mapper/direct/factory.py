from src.db.models.base import FamilyModel
from src.nlp_processor.jobs.mapper.direct.base import DirectJobResultMapperBase
from src.nlp_processor.jobs.result.base import JobResultBase

def get_type_value_mapper(model: type[FamilyModel]) -> type[DirectJobResultMapperBase]:

    class TypeValueMapper(DirectJobResultMapperBase):

        async def map(
            self,
            result: JobResultBase,
            url_id: int
        ) -> list[FamilyModel]:
            return [model(
                url_id=url_id,
                type=result.job_id.job_type.value,
                value=result.result
            )]

    TypeValueMapper.__name__ = f"{model.__name__}JobMapper"

    return TypeValueMapper