from datetime import datetime

from app.main import app
from app.db.models import Transcription
from app.db.database import get_db


def test_transcribe_file(client, db_session):
    def get_db_override():
        return db_session

    app.dependency_overrides[get_db] = get_db_override

    t1 = Transcription(file_name="test1.wav",
                       transcription="Hello world", created_at=datetime.now())
    t2 = Transcription(file_name="test2.wav",
                       transcription="Another one", created_at=datetime.now())
    db_session.add(t1)
    db_session.add(t2)
    db_session.commit()

    response = client.get("/v1/transcriptions")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["file_name"] in ["test1.wav", "test2.wav"]
    assert "transcription" in data[0]
