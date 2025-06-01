from typing import TypeVar, Generic

import pandas as pd
from pydantic import BaseModel

from src.shared.bases.pydantic.df_labels import DataFrameLabelsBase


# Type variable bounded to LabelSet
LabelType = TypeVar("LabelType", bound=DataFrameLabelsBase)


class LabeledDataFrame(BaseModel, Generic[LabelType]):
    """
    A pandas DataFrame along with column labels
    """
    df: pd.DataFrame
    labels: LabelType

    class Config:
        arbitrary_types_allowed = True
        frozen = True  # optional: makes the model immutable