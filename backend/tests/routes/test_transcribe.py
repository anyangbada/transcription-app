import os
from unittest.mock import patch


def test_transcribe_file(client):
    audio_path = os.path.join("tests", "assets", "sample.wav")

    with patch("app.routes.transcribe.transcriber.transcribe") as mock_transcribe:
        mock_transcribe.return_value = "mocked transcription"

        with open(audio_path, "rb") as f:
            response = client.post(
                "/transcribe", files={"files": ("sample.wav", f, "audio/wav")})

        assert response.status_code == 200
        result = response.json()[0]
        assert result["transcription"] == "mocked transcription"
        assert result["file_name"] == "sample.wav"
