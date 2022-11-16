from pydantic import BaseModel, Extra


class Country(BaseModel):
    name: str
    confirmed: int
    deaths: int
    last_updated_by_source_at: str

    class Config:
        extra = Extra.forbid
