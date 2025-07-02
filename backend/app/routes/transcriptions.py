from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Transcription
from app.schemas.transcriptions import TranscriptionOut

router = APIRouter()


@router.get("/v1/transcriptions", response_model=list[TranscriptionOut])
def get_all_transcriptions(db: Session = Depends(get_db)):
    transcriptions = db.query(Transcription).order_by(
        Transcription.created_at.desc()).all()
    return transcriptions
