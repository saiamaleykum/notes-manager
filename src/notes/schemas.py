from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class Tag(BaseModel):
    id: int
    name: str


class NoteCreate(BaseModel):
    title: str
    content: str
    tags: List[str]

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    tags: List[Tag]

    class Config:
        from_attributes = True