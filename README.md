# Data Analysis



# Setup

```bash
uv sync
python -m spacy download en_core_web_trf
docker compose up -d
alembic upgrade head
```


# Steps

1. Gather URLs from dataset
`python core/pipeline/1_get_dataset_urls.py`
2. Get HTML from URLs
`python core/pipeline/2_fetch_html.py`
3. Process HTML data
`python core/pipeline/3_process_data.py`