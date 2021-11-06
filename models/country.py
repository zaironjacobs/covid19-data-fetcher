from pydantic import BaseModel, Extra


class Country(BaseModel):
    name: str
    confirmed: int
    deaths: int
    active: int
    recovered: int
    last_updated_by_source_at: str

    class Config:
        extra = Extra.forbid
