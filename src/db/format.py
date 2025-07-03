from enum import Enum

from sqlalchemy import Row


def row_to_simple_dict(row: Row) -> dict[str, str | int | float | bool]:
    """Converts a database row to a dictionary with only string and numeric values"""
    return {
        key: (value.value if isinstance(value, Enum) else value)
        for key, value in row._asdict().items()  # for SQLAlchemy Row
    }

def rows_to_list_of_simple_dicts(rows: list[Row]) -> list[dict[str, str | int | float | bool]]:
    return [row_to_simple_dict(row) for row in rows]