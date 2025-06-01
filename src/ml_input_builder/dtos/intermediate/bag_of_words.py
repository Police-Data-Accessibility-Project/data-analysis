import pandas as pd
from scipy.sparse import csr_matrix

from src.shared.bases.pydantic.arbitrary_base_model import ArbitraryBaseModel
import numpy as np
import numpy.typing as npt

class BagOfWordsIntermediate(ArbitraryBaseModel):
    sparse_matrix: csr_matrix
    urls_ids: npt.NDArray[np.int_]
    terms_ids: npt.NDArray[np.int_]
    y_relevant: pd.Series
    y_fine: pd.Series
    y_coarse: pd.Series