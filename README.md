# Audio Transcript & Sentiment Analysis API

A FastAPI backend that transcribes audio files using Whisper and analyzes sentiment using Google Gemini API.

## Features

- Upload audio files via REST API
- Automatic transcription using OpenAI Whisper (local model)
- Sentiment analysis using Google Gemini API
- Returns transcript, sentiment (Positive/Negative/Neutral), and confidence score

## Quick Start

### 1. Create Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variable

Set your Google Gemini API key:

```bash
export GEMINI_API_KEY="your-api-key-here"
export ASSEMBLYAI_API_KEY="key"
```

Or create a `.env` file:

```
GEMINI_API_KEY=your-api-key-here
ASSEMBLYAI_API_KEY=key
```

### 5. Start the Server

Open a terminal and run:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 6. Start Streamlit Frontend

Open another terminal (keep the server running), activate the venv, and run:

```bash
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

streamlit run streamlit_app.py
```

The Streamlit app will open in your browser at `http://localhost:8501`

## API Endpoints

### POST /process-audio

Upload an audio file for transcription and sentiment analysis.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: audio file (form field: `file`)

**Response:**
```json
{
  "transcript": "I am very unhappy with your service.",
  "sentiment": "Negative",
  "confidence": 0.92
}
```

**Error Responses:**
- If transcription fails:
```json
{
  "transcript": "",
  "sentiment": "",
  "confidence": 0.0,
  "error": "transcription_error"
}
```

- If sentiment analysis fails:
```json
{
  "transcript": "transcribed text here",
  "sentiment": "",
  "confidence": 0.0,
  "error": "sentiment_error"
}
```

### GET /

Root endpoint - returns API information

### GET /health

Health check endpoint

## Testing

You can test the API using curl:

```bash
curl -X POST "http://localhost:8000/process-audio" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-audio-file.mp3"
```

Or using Python requests:

```python
import requests

url = "http://localhost:8000/process-audio"
files = {"file": open("your-audio-file.mp3", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## Streamlit Frontend

A user-friendly web interface is available using Streamlit. See **Quick Start** section above for setup instructions.

### Features

- Drag-and-drop audio file upload
- Real-time processing status
- Display transcript and sentiment analysis
- Visual confidence indicators
- API health check

**Note:** Make sure the FastAPI backend is running before starting Streamlit (see step 5 in Quick Start).

## Project Structure

```
/app
  main.py              # FastAPI application and endpoint
  whisper_service.py   # Whisper transcription service
  gemini_service.py    # Gemini sentiment analysis service
streamlit_app.py       # Streamlit frontend application
requirements.txt       # Python dependencies
README.md             # This file
```

## Notes

- The Whisper "small" model is loaded once at startup
- Audio files are saved temporarily and cleaned up after processing
- Make sure you have sufficient disk space for temporary files
- The API handles errors gracefully without crashing the server
- Streamlit frontend requires the FastAPI backend to be running

