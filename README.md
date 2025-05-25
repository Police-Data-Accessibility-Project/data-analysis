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
2. Get URL Annotations
`python core/pipeline/2_get_url_annotations.py`
3. Get HTML from URLs
`python core/pipeline/3_fetch_html.py`
4. Process HTML data
`python core/pipeline/4_process_data.py`