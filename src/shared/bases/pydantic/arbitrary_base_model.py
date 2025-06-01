from pydantic import BaseModel


class ArbitraryBaseModel(BaseModel):
    """A shorthand for pydantic's BaseModel that allows arbitrary types."""
    class Config:
        arbitrary_types_allowed = True