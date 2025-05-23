from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Optional

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Mapped

from core.database_logic.enums import ErrorType
from core.database_logic.model_helpers import get_id_column_orm, get_created_at_column_orm, get_url_id_column_orm, \
    get_enum_column_orm
from core.nlp_processor.v2.jobs.enums import HTMLContentMetricJobType, HTMLMetadataJobType, URLComponentJobType, \
    HTMLBagOfWordsJobType

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
    compressed_html = sa.orm.relationship(
        "URLCompressedHTML", back_populates="url", uselist=False, cascade="all, delete-orphan"
        )
    components = sa.orm.relationship("URLComponent", back_populates="url", cascade="all, delete-orphan")
    html_metadata = sa.orm.relationship("HTMLMetadata", back_populates="url", cascade="all, delete-orphan")
    html_content_metrics = sa.orm.relationship("HTMLContentMetric", back_populates="url", cascade="all, delete-orphan")
    html_bag_of_words = sa.orm.relationship("HTMLBagOfWords", back_populates="url", cascade="all, delete-orphan")


class FamilyModel(Base):
    __abstract__ = True
    id: Mapped[int] = get_id_column_orm()
    url_id: Mapped[int] = get_url_id_column_orm()
    created_at: Mapped[datetime] = get_created_at_column_orm()

    @property
    @abstractmethod
    def type(self) -> Enum:
        pass

    @property
    @abstractmethod
    def value(self) -> Any:
        pass

    @property
    @abstractmethod
    def url(self) -> URL:
        pass


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


class URLComponent(FamilyModel):
    __tablename__ = "url_components"
    type: Mapped[URLComponentJobType] = get_enum_column_orm(
        URLComponentJobType,
        enum_name="url_component_type",
    )
    value = sa.Column(sa.Text, nullable=True)

    # Relationships
    url = get_single_url_relationship("components")


class HTMLMetadata(FamilyModel):
    __tablename__ = "html_metadata"
    type: Mapped[HTMLMetadataJobType] = get_enum_column_orm(
        HTMLMetadataJobType,
        enum_name="html_metadata_type",
    )
    value = sa.Column(sa.Text, nullable=True)

    # Relationships
    url = get_single_url_relationship("html_metadata")


class HTMLContentMetric(FamilyModel):
    __tablename__ = "html_content_metrics"
    type: Mapped[HTMLContentMetricJobType] = get_enum_column_orm(
        HTMLContentMetricJobType,
        enum_name="html_content_metric_type",
    )
    value = sa.Column(sa.Integer, nullable=False)

    # Relationships
    url = get_single_url_relationship("html_content_metrics")

class HTMLBagOfWords(FamilyModel):
    __tablename__ = "html_bag_of_words"
    type: Mapped[HTMLBagOfWordsJobType] = get_enum_column_orm(
        HTMLBagOfWordsJobType,
        enum_name="html_bag_of_words_type",
    )
    term: Mapped[Optional[str]] = sa.Column(sa.Text, nullable=True)
    count = sa.Column(sa.Integer, nullable=False)

    # Relationships
    url = get_single_url_relationship("html_bag_of_words")