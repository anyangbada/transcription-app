import asyncio
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, UploadFile, File, Depends

import shutil
import os
from sqlalchemy.orm import Session
from fastapi.concurrency import run_in_threadpool

from app.db.operations import save_transcription
from app.db.database import get_db
from app.core.config import settings
from app.service.transcriber import transcribe_and_save

router = APIRouter()


@router.post("/transcribe")
async def transcribe_audio(background_tasks: BackgroundTasks, files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    if not all(file.filename.endswith((".wav", ".mp3", ".m4a")) for file in files):
        raise HTTPException(
            status_code=400, detail="unsupported file format")

    batch = {}
    for file in files:
        file_path = os.path.join(settings.audio_dir, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        transcription = save_transcription(file.filename, "", db)

        batch[transcription.id] = file_path

    # async process
    for tid, fpath in batch.items():
        background_tasks.add_task(
            transcribe_and_save, tid, fpath, db)

    return {"message": f"saved files: {len(files)}"}
