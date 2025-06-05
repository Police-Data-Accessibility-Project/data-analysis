from typing import TypeVar, Generic

import polars as pl
from pydantic import BaseModel

from src.shared.bases.pydantic.df_labels import DataFrameLabelsBase


# Type variable bounded to LabelSet
LabelType = TypeVar("LabelType", bound=DataFrameLabelsBase)


class LabeledDataFrame(BaseModel, Generic[LabelType]):
    """
    A polars DataFrame along with column labels
    """
    df: pl.DataFrame
    labels: LabelType

    class Config:
        arbitrary_types_allowed = True
        frozen = True  # optional: makes the model immutable