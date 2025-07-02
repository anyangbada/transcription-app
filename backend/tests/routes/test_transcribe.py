import io
import os

from unittest.mock import patch


def test_transcribe_file(client):
    audio_path = os.path.join("tests", "assets", "sample.wav")

    with patch("app.service.transcriber.transcribe_and_save") as mock_transcribe:
        mock_transcribe.return_value = "mocked transcription"

        # Simulate an in-memory file
        file_content = b"fake audio data"
        files = [
            ("files", ("test.wav", io.BytesIO(file_content), "audio/wav")),
            ("files", ("hello.mp3", io.BytesIO(file_content), "audio/mp3")),
        ]

        response = client.post("/v1/transcribe", files=files)

        assert response.status_code == 200
        assert response.json()["message"] == "saved files: 2"
