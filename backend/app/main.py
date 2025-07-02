from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health_check, transcribe, transcriptions, search
from app.db.database import init_db
from app.core.config import settings
from app.core.whisper import init_whisper_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    init_whisper_model()

    yield

app = FastAPI(lifespan=lifespan)

# Allow CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_check.router, tags=["Health"])
app.include_router(transcribe.router, tags=["Transcribe"])
app.include_router(transcriptions.router, tags=["Transcriptions"])
app.include_router(search.router, tags=["Search"])

os.makedirs(settings.audio_dir, exist_ok=True)
