# huggingface-trainer



# Setup

```bash
uv sync
python -m spacy download en_core_web_sm
docker compose up -d
alembic upgrade head
```


# Steps

1. Gather URLs from dataset
`python core/hugging_face/get_dataset_urls.py`
2. Get HTML from URLs
`python core/scraper/fetch_html.py`
3. Process HTML data
`python core/nlp_processor/process_html.py`