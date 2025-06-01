from dataclasses import dataclass

from src.shared.bases.pydantic.df_labels import DataFrameLabelsBase

@dataclass(frozen=True)
class BagOfWordsBaseLabels(DataFrameLabelsBase):
    """
    Labels used by the data frame in the bag of words process
    """

    # Initial SQLAlchemy column names
    url_id: str = "url_id"
    term_id: str = "term_id"
    tf_idf: str = "tf_idf"
    relevant: str = "relevant"
    record_type_fine: str = "record_type_fine"
    record_type_coarse: str = "record_type_coarse"
