from src.ml_input_builder.registry.entry import DatasetRegistryEntry

BAG_OF_WORDS_REGISTRY_ENTRY = DatasetRegistryEntry(
    filename="bag_of_words.parquet",
    repo_id="PDAP/data_sources_bag_of_words",
)
RAW_REGISTRY_ENTRY = DatasetRegistryEntry(
    filename="raw.parquet",
    repo_id="PDAP/data_sources_raw",
)