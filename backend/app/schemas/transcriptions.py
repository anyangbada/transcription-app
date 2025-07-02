from pydantic import BaseModel
from datetime import datetime


class TranscriptionOut(BaseModel):
    file_name: str
    transcription: str
    created_at: datetime

    class Config:
        orm_mode = True
