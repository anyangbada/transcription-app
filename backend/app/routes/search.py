from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Transcription
from app.schemas.transcriptions import TranscriptionOut

router = APIRouter()


@router.get("/search", response_model=list[TranscriptionOut])
def search_transcriptions(
    file_name: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    results = db.query(Transcription).filter(
        Transcription.file_name.ilike(f"%{file_name}%")
    ).order_by(Transcription.created_at.desc()).all()
    return results
