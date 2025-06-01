from dataclasses import dataclass

from src.db.df_labels.bag_of_words import BagOfWordsBaseLabels
from src.ml_input_builder.df_labels.bag_of_words.indexing import BagOfWordsIndexingLabels
from src.shared.bases.pydantic.df_labels import DataFrameLabelsBase

@dataclass(frozen=True)
class BagOfWordsCombinedLabels(DataFrameLabelsBase):
    base: BagOfWordsBaseLabels
    idx: BagOfWordsIndexingLabels

    @classmethod
    def from_base(cls, base: BagOfWordsBaseLabels) -> "BagOfWordsCombinedLabels":
        if not isinstance(base, BagOfWordsBaseLabels):
            raise TypeError(f"Expected BagOfWordsBaseLabels, got {type(base).__name__}")
        return cls(
            base=base,
            idx=BagOfWordsIndexingLabels()
        )