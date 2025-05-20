from datetime import datetime

from sqlalchemy.orm import declarative_base, Mapped, relationship
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

    # Relationships
    errors = sa.orm.relationship("URLError", back_populates="url", cascade="all, delete-orphan")
    full_html = sa.orm.relationship("URLFullHTML", back_populates="url", uselist=False, cascade="all, delete-orphan")
    compressed_html = sa.orm.relationship("URLCompressedHTML", back_populates="url", uselist=False, cascade="all, delete-orphan")
    components = sa.orm.relationship("URLComponent", back_populates="url", cascade="all, delete-orphan")
    html_metadata = sa.orm.relationship("HTMLMetadata", back_populates="url", cascade="all, delete-orphan")

def get_single_url_relationship(back_populates_name: str) -> Mapped[URL]:
    return sa.orm.relationship("URL", back_populates=back_populates_name, uselist=False)

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

    # Relationships
    url = get_single_url_relationship("errors")

class URLFullHTML(Base):
    __tablename__ = "url_full_html"
    id: Mapped[int] = get_id_column_orm()
    url_id: Mapped[int] = get_url_id_column_orm()
    html = sa.Column(sa.Text, nullable=False)
    created_at: Mapped[datetime] = get_created_at_column_orm()
    updated_at: Mapped[datetime] = get_created_at_column_orm()

    # Relationships
    url = get_single_url_relationship("full_html")

class URLCompressedHTML(Base):
    __tablename__ = "url_compressed_html"
    id: Mapped[int] = get_id_column_orm()
    url_id: Mapped[int] = get_url_id_column_orm()
    compressed_html = sa.Column(sa.LargeBinary, nullable=False)
    created_at: Mapped[datetime] = get_created_at_column_orm()

    # Relationships
    url = get_single_url_relationship("compressed_html")

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

    # Relationships
    url = get_single_url_relationship("components")

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

    # Relationships
    url = get_single_url_relationship("html_metadata")