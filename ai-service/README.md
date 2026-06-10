# MindCare AI Service

This folder now contains a FastAPI text emotion analysis service using spaCy.
The service is designed to replace the backend demo sentiment logic with a real Python AI endpoint.

## Install

1. Create a Python environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2. Install dependencies
```powershell
pip install -r requirements.txt
```
3. Install the spaCy model
```powershell
python -m spacy download en_core_web_sm
```

## Run

```powershell
uvicorn main:app --reload --port 8001
```

## Endpoints

- `GET /health` - service health check
- `POST /analyze/text` - analyze text emotion

### Example request

```json
POST /analyze/text
{
  "text": "I am feeling overwhelmed and anxious about exams."
}
```

### Example response

```json
{
  "source": "text",
  "text": "I am feeling overwhelmed and anxious about exams.",
  "emotion": "stress",
  "sentiment": "negative",
  "risk": "high",
  "confidence": 84,
  "scores": {
    "joy": 0,
    "sadness": 0,
    "anger": 0,
    "fear": 1,
    "stress": 1,
    "surprise": 0,
    "neutral": 0
  }
}
```

## Next step

Integrate this service with the backend chat flow so `/api/chat/message` uses the new spaCy analysis instead of the in-memory demo logic.
