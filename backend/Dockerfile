# Base image with Python
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install system dependencies for torchaudio
RUN apt-get update && apt-get install -y \
    libsndfile1 ffmpeg git && \
    apt-get clean

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy only dependency files first (enables caching)
COPY pyproject.toml poetry.lock /app/

# Install dependencies (this will be cached unless the above files change)
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the rest of your app
COPY . /app

# Expose port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
