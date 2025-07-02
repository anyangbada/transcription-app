import os


def test_transcribe_file(client):
    audio_path = os.path.join("tests", "assets", "sample.wav")
    with open(audio_path, "rb") as f:
        response = client.post(
            "/transcribe", files={"files": ("sample.wav", f, "audio/wav")})
    assert response.status_code == 200
    result = response.json()[0]
    assert "file_name" in result
    assert "transcription" in result
