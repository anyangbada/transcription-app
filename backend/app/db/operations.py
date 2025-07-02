from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import Transcription
from app.db.database import get_db
from app.core.config import logger


def save_transcription(
    file_name: str,
    transcription: str,
    db: Session = Depends(get_db),
) -> Transcription:
    transcription = Transcription(
        file_name=file_name,
        transcription=transcription
    )
    db.add(transcription)
    db.commit()
    db.refresh(transcription)
    return transcription


def update_transcription_text_by_id(
    id: int,
    text: str,
    db: Session = Depends(get_db),
) -> Transcription | None:
    transcription = db.query(Transcription).filter(
        Transcription.id == id).first()

    if transcription is None:
        logger.error(f"transcription with id={id} not found")
        return None

    transcription.transcription = text
    db.commit()
    db.refresh(transcription)
    return transcription


def get_all_transcriptions(db: Session = Depends(get_db)):
    return db.query(Transcription).all()
