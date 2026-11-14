from pydantic import BaseModel


class APower(BaseModel):
    id: str


class Stats(BaseModel):
    status: int


class Gateway(BaseModel):
    id: str
    name: str
    aPower: list[APower] = []
    stats: Stats = Stats(status=1)
