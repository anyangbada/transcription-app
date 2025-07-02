from app.db.operations import update_transcription_text_by_id
from app.core.config import logger
from app.core.whisper import transcriber


def transcribe_and_save(id: int, file_path: str, db) -> None:
    logger.debug(f"start trascribing {id} from {file_path}")
    result = transcriber.transcribe(file_path)
    update_transcription_text_by_id(id, result, db)
    logger.debug(f"updated transcription {id}: {result}")
