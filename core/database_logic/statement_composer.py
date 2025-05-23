from enum import Enum
from typing import Type

from sqlalchemy import func, case, ColumnElement
from sqlalchemy.orm import InstrumentedAttribute

from core.database_logic.enums import ComponentType, HTMLMetadataType, HTMLContentMetricType
from core.database_logic.models import URLComponent, HTMLMetadata, HTMLContentMetric




class StatementComposer:

    @staticmethod
    def bool_or_case(attribute: InstrumentedAttribute, enum: Enum):
        return func.bool_or(
            case(
                (attribute == enum.value, True),
                else_=False
            )
        ).label(f"has_{enum.value}")


    @staticmethod
    def url_component_type_exists(
        type_name: ComponentType,
    ):
        return StatementComposer.bool_or_case(URLComponent.type, type_name)

    @staticmethod
    def url_html_metadata_type_exists(
        type_name: HTMLMetadataType,
    ):
        return StatementComposer.bool_or_case(HTMLMetadata.type, type_name)

class ExistsQueryCreator:

    def __init__(
        self,
        attribute: InstrumentedAttribute,
        valid_enums: Type[Enum] or list[Enum],
    ):
        self.enum_class = valid_enums
        self.attribute = attribute

    def select(self) -> list:
        return [StatementComposer.bool_or_case(self.attribute, enum) for enum in self.enum_class]

    def where(self) -> list:
        return [
            StatementComposer.bool_or_case(self.attribute, enum) == True for enum in self.enum_class
        ]