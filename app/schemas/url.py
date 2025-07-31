from pydantic import BaseModel, HttpUrl
from uuid import UUID
from datetime import datetime

class URLCreate(BaseModel):
    target_url: HttpUrl

class URLInfo(BaseModel):
    id: UUID
    short_code: str
    target_url: HttpUrl
    clicks: int
    created_at: datetime

    class Config:
        orm_mode = True
