from datetime import datetime

from pydantic import UUID4, BaseModel, Field


class EntryBase(BaseModel):
    title: str = Field(max_length=64)
    body: str = Field(max_length=1024)


class EntryInCreate(EntryBase):
    pass


class EntryInResponse(EntryInCreate):
    id: UUID4
    created: datetime

    class Config:
        orm_mode = True
