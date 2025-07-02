# 📝 Transcription App

A full-stack application that enables users to upload audio files and transcribe them using the Whisper model. It supports transcription history, file name search, and a responsive frontend.

---

## Getting Started

To build and run the app using Docker Compose:

```bash
docker-compose up --build
```

### Access the Services

- **Frontend UI**: [http://localhost:3000](http://localhost:3000)  
- **Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)  
- **Health Check Endpoint**: [http://localhost:8000/health](http://localhost:8000/health)

---

## Development Mode

You can run the frontend and backend separately for development.

### Backend

```bash
cd backend
poetry install
poetry shell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend/app
npm install
npm start
```

---

## Running Tests

### Backend Tests

```bash
cd backend
pytest tests
```

### Frontend Tests

```bash
cd frontend/app
npm run test
```

---

## Project Structure

```
transcription-app/
├── backend/              # FastAPI + Whisper backend
│   └── app/
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── models/
│       ├── service/
│       └── main.py
├── frontend/             # React frontend
│   └── app/
│       ├── src/
│       ├── public/
│       └── package.json
├── docker-compose.yml
└── README.md
```

---

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy, SQLite, HuggingFace Whisper
- **Frontend**: React, Material UI, Axios
- **Containerization**: Docker, Docker Compose
- **Testing**: Pytest, Jest + React Testing Library

---

## Assumptions

- Audio files must be in supported formats (`.wav`, `.mp3`, etc.)
- Whisper model used: `openai/whisper-tiny` via Hugging Face
- Database: Local SQLite, in-memory for tests

---

## Backend API Specification

### Endpoints

#### `GET /health`

- **Description:** Health check endpoint to verify if the service is running.
- **Response:**
```json
{
  "status": "ok"
}
```

---

#### `POST /v1/transcribe`

- **Description:** Accepts one or more audio files and process asynchonous transcription. Results are saved in the database.
- **Request:**
  - Content-Type: `multipart/form-data`
  - Form field: `files` (supports multiple files)
- **Response:**
```json
[
  {
    "message": "saved files: 1"
  }
]
```

---

#### `GET /v1/transcriptions`

- **Description:** Retrieve all transcription records stored in the database.
- **Response:**
```json
[
  {
    "file_name": "sample1.wav",
    "transcription": "This is a transcribed text.",
    "created_at": "2025-06-30T10:12:30Z"
  },
  {
    "file_name": "sample2.wav",
    "transcription": "Another text.",
    "created_at": "2025-06-30T10:15:42Z"
  }
]
```

---

#### `GET /v1/search?file_name=sample`

- **Description:** Search transcriptions by (partial or full) file name.
- **Query Parameter:**
  - `file_name` – audio file name (case-insensitive, partial match supported)
- **Response:**
```json
[
  {
    "file_name": "sample1.wav",
    "transcription": "This is a transcribed text.",
    "created_at": "2025-06-30T10:12:30Z"
  }
]
```

---