from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Optional

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Mapped

from core.db.enums import ErrorType, RecordTypeFine, RecordTypeCoarse
from core.db.models.helpers import get_id_column_orm, get_created_at_column_orm, get_url_id_column_orm, \
    get_enum_column_orm
from core.nlp_processor.jobs.enums import HTMLContentMetricJobType, HTMLMetadataJobType, URLComponentJobType, \
    HTMLBagOfWordsJobType, HTMLTermTagCountsJobType

Base = declarative_base()

url_relationship_kwargs = dict(
    cascade="all, delete-orphan",
    back_populates="url"
)

class URL(Base):
    __tablename__ = "urls"
    id: Mapped[int] = get_id_column_orm()
    url = sa.Column(sa.String, unique=True, index=True)
    response_code = sa.Column(sa.Integer, nullable=True)
    created_at: Mapped[datetime] = get_created_at_column_orm()

    # Relationships
    errors = sa.orm.relationship("URLError", **url_relationship_kwargs)
    full_html = sa.orm.relationship("URLFullHTML", uselist=False, **url_relationship_kwargs)
    compressed_html = sa.orm.relationship(
        "URLCompressedHTML", uselist=False, **url_relationship_kwargs
        )
    components = sa.orm.relationship("URLComponent", **url_relationship_kwargs)
    html_metadata = sa.orm.relationship("HTMLMetadata", **url_relationship_kwargs)
    html_content_metrics = sa.orm.relationship("HTMLContentMetric", **url_relationship_kwargs)
    html_bag_of_words = sa.orm.relationship("HTMLBagOfWords", **url_relationship_kwargs)
    html_term_tag_counts = sa.orm.relationship("HTMLTermTagCount", **url_relationship_kwargs)
    annotations = sa.orm.relationship("URLAnnotations", **url_relationship_kwargs)

class URLDerivedModel(Base):
    __abstract__ = True
    id: Mapped[int] = get_id_column_orm()
    url_id: Mapped[int] = get_url_id_column_orm()
    created_at: Mapped[datetime] = get_created_at_column_orm()

class StringMapModel(Base):
    __abstract__ = True
    id: Mapped[int] = get_id_column_orm()
    name: Mapped[str] = sa.Column(sa.Text, nullable=False)


class FamilyModel(URLDerivedModel):
    __abstract__ = True

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

class URLAnnotations(URLDerivedModel):
    __tablename__ = 'url_annotations'
    relevant: Mapped[bool] = sa.Column(sa.Boolean, nullable=False)
    record_type_fine: Mapped[RecordTypeFine] = get_enum_column_orm(
        enum_class=RecordTypeFine,
        enum_name="url_annotations_fine_record_type",
        nullable=False
    )
    record_type_coarse: Mapped[RecordTypeCoarse] = get_enum_column_orm(
        enum_class=RecordTypeCoarse,
        enum_name="url_annotations_coarse_record_type",
        nullable=False
    )

    # Relationships
    url = get_single_url_relationship("annotations")

class URLError(URLDerivedModel):
    __tablename__ = "url_errors"
    error_type: Mapped[ErrorType] = get_enum_column_orm(
        enum_class=ErrorType,
        enum_name="error_type",
        nullable=False
    )
    error = sa.Column(sa.Text, nullable=False)

    # Relationships
    url = get_single_url_relationship("errors")


class URLFullHTML(URLDerivedModel):
    __tablename__ = "url_full_html"
    html = sa.Column(sa.Text, nullable=False)
    updated_at: Mapped[datetime] = get_created_at_column_orm()

    # Relationships
    url = get_single_url_relationship("full_html")


class URLCompressedHTML(URLDerivedModel):
    __tablename__ = "url_compressed_html"
    compressed_html = sa.Column(sa.LargeBinary, nullable=False)

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

class HTMLTag(StringMapModel):
    __tablename__ = "html_tags"

    # Relationships
    term_tag_counts = sa.orm.relationship("HTMLTermTagCount", back_populates="tag")

class HTMLTerm(StringMapModel):
    __tablename__ = "html_terms"

    # Relationships
    term_tag_counts = sa.orm.relationship("HTMLTermTagCount", back_populates="term")

class HTMLTermTagCount(FamilyModel):
    __tablename__ = "html_term_tag_counts"
    type: Mapped[HTMLTermTagCountsJobType] = get_enum_column_orm(
        HTMLTermTagCountsJobType,
        enum_name='html_term_tag_counts_type',
    )
    tag_id: Mapped[Optional[int]] = sa.Column(
        sa.Integer,
        sa.ForeignKey('html_tags.id'),
        nullable=True
    )
    term_id: Mapped[Optional[int]] = sa.Column(
        sa.Integer,
        sa.ForeignKey('html_terms.id'),
        nullable=True
    )
    count = sa.Column(sa.Integer, nullable=False)

    # Relationships
    url = get_single_url_relationship("html_term_tag_counts")
    tag = sa.orm.relationship("HTMLTag", uselist=False)
    term = sa.orm.relationship("HTMLTerm", uselist=False)