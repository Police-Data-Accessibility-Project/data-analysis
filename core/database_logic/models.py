from datetime import datetime

from sqlalchemy.orm import declarative_base, Mapped
import sqlalchemy as sa

from core.database_logic.enums import ComponentType, ErrorType, HTMLMetadataType
from core.database_logic.model_helpers import get_id_column_orm, get_created_at_column_orm, get_url_id_column_orm, \
    get_enum_column_orm

Base = declarative_base()


class URL(Base):
    __tablename__ = "urls"
    id: Mapped[int] = get_id_column_orm()
    url = sa.Column(sa.String, unique=True, index=True)
    response_code = sa.Column(sa.Integer, nullable=True)
    created_at: Mapped[datetime] = get_created_at_column_orm()

class URLError(Base):
    __tablename__ = "url_errors"
    id: Mapped[int] = get_id_column_orm()
    url_id: Mapped[int] = get_url_id_column_orm()
    error_type: Mapped[ErrorType] = get_enum_column_orm(
        enum_class=ErrorType,
        enum_name="error_type",
        nullable=False
    )
    error = sa.Column(sa.Text, nullable=False)
    created_at: Mapped[datetime] = get_created_at_column_orm()

class URLFullHTML(Base):
    __tablename__ = "url_full_html"
    id: Mapped[int] = get_id_column_orm()
    url_id: Mapped[int] = get_url_id_column_orm()
    html = sa.Column(sa.Text, nullable=False)
    created_at: Mapped[datetime] = get_created_at_column_orm()
    updated_at: Mapped[datetime] = get_created_at_column_orm()

class URLComponent(Base):
    __tablename__ = "url_components"
    id: Mapped[int] = get_id_column_orm()
    url_id: Mapped[int] = get_url_id_column_orm()
    type: Mapped[ComponentType] = get_enum_column_orm(
        ComponentType,
        enum_name="url_component_type",
    )
    value = sa.Column(sa.Text, nullable=True)
    created_at: Mapped[datetime] = get_created_at_column_orm()

class HTMLMetadata(Base):
    __tablename__ = "html_metadata"
    id: Mapped[int] = get_id_column_orm()
    url_id: Mapped[int] = get_url_id_column_orm()
    type: Mapped[HTMLMetadataType] = get_enum_column_orm(
        HTMLMetadataType,
        enum_name="html_metadata_type",
    )
    value = sa.Column(sa.Text, nullable=True)
    created_at: Mapped[datetime] = get_created_at_column_orm()