from pydantic import BaseModel, Extra


class Article(BaseModel):
    title: str
    source_name: str
    author: str
    description: str
    url: str
    published_at: str

    class Config:
        extra = Extra.forbid
