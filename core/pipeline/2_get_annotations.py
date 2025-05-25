"""
Get annotations from URLs and add them to the database
"""

import asyncio

from datasets import load_dataset

from core.constants import TRAINING_URLS_HF_NAME
from core.db.client import DatabaseClient
from core.db.dtos.input.url_annotations import URLAnnotationsInput


def load_url_annotations_from_huggingface(dataset_name: str) -> list[URLAnnotationsInput]:
    ds = load_dataset(dataset_name)
    inputs_ = []
    for row in ds['train']:
        if row["url"] is None:
            continue
        relevant_str = row["relevant"]
        if relevant_str == "Yes":
            relevant = True
        elif relevant_str == "No":
            relevant = False
        else:
            continue
        input_ = URLAnnotationsInput(
            url=row["url"],
            relevant=relevant,
            record_type_fine=row["record_type"],
            record_type_coarse=row["coarse_record_type"],
        )
        inputs_.append(input_)
    return inputs_

if __name__ == "__main__":
    inputs = load_url_annotations_from_huggingface(TRAINING_URLS_HF_NAME)
    dbc = DatabaseClient()
    asyncio.run(dbc.add_annotations(inputs))
