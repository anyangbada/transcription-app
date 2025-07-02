from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.database import Base


class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False, index=True)
    transcription = Column(String)
    created_at = Column(DateTime, default=datetime.now())
