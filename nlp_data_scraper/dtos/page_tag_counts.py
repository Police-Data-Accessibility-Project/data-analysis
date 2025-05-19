from pydantic import BaseModel


class PageTagCounts(BaseModel):
    img: int = 0
    a: int = 0
    p: int = 0
    span: int = 0
    div: int = 0
    li: int = 0
    ul: int = 0
    ol: int = 0
    table: int = 0
    tr: int = 0
    td: int = 0
    th: int = 0
    h1: int = 0
    h2: int = 0
    h3: int = 0
    h4: int = 0
    h5: int = 0
    h6: int = 0
    form: int = 0
    input: int = 0
    button: int = 0
    meta: int = 0