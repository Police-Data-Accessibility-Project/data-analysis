"""
Logic for writing data to disk
"""


import polars as pl

from src.utils.paths import get_output_path


def write_to_parquet(df: pl.DataFrame, name: str) -> None:

    df.write_parquet(get_output_path(name))

