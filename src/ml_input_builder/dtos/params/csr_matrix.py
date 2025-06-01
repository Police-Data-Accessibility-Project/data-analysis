from typing import Tuple

import numpy as np
from pydantic import field_validator
from scipy.sparse import csr_matrix

from src.shared.bases.pydantic.arbitrary_base_model import ArbitraryBaseModel


class CSRMatrixParams(ArbitraryBaseModel):
    data: np.ndarray
    row: np.ndarray
    col: np.ndarray
    shape: Tuple[int, int]

    @field_validator("data", "row", "col", mode="before")
    def coerce_array(cls, v):
        return np.array(v)

    def to_csr(self) -> csr_matrix:
        return csr_matrix(
            (
                np.array(self.data),
                (self.row, self.col)
            ),
            shape=self.shape
        )