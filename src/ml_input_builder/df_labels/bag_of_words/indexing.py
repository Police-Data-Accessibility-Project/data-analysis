from src.shared.bases.pydantic.df_labels import DataFrameLabelsBase


class BagOfWordsIndexingLabels(DataFrameLabelsBase):
    """
    Includes the column names for indexing labels added later
    """
    url_idx: str = "url_idx"
    term_idx: str = "term_idx"