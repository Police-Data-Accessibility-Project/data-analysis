from sqlalchemy import func, case

from core.database_logic.enums import ComponentType, HTMLMetadataType
from core.database_logic.models import URLComponent, HTMLMetadata


class StatementComposer:

    @staticmethod
    def url_component_type_exists(
        type_name: ComponentType,
    ):
        return func.bool_or(
            case(
                (URLComponent.type == type_name.value, True),
                else_=False
            )
        ).label(f"has_{type_name.value}")

    @staticmethod
    def url_html_metadata_type_exists(
        type_name: HTMLMetadataType,
    ):
        return func.bool_or(
            case(
                (HTMLMetadata.type == type_name.value, True),
                else_=False
            )
        ).label(f"has_{type_name.value}")