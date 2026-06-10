from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Literal
import spacy

app = FastAPI(title="MindCare AI Text Emotion Service")

try:
    nlp = spacy.load("en_core_web_sm")
except OSError as exc:
    raise RuntimeError(
        "spaCy model 'en_core_web_sm' is not installed. "
        "Run: python -m spacy download en_core_web_sm"
    ) from exc

class TextAnalysisRequest(BaseModel):
    text: str

class TextAnalysisResponse(BaseModel):
    source: Literal["text"]
    emotion: str
    sentiment: str
    risk: str
    confidence: int
    scores: Dict[str, int]
    text: str

EMOTION_LEXICON = {
    "joy": ["happy", "joy", "excited", "grateful", "content", "positive", "good", "nice", "smile", "calm"],
    "sadness": ["sad", "down", "depressed", "unhappy", "lonely", "cry", "tear", "gloomy", "hurt", "loss"],
    "anger": ["angry", "mad", "furious", "irritated", "annoyed", "rage", "hate", "upset", "resentful"],
    "fear": ["anxious", "worried", "scared", "afraid", "fearful", "panic", "nervous", "fear", "terrified"],
    "stress": ["stressed", "pressure", "overwhelmed", "burnout", "tired", "exhausted", "strain", "panic"],
    "surprise": ["surprised", "shocked", "amazed", "startled", "unexpected"],
    "neutral": ["okay", "fine", "neutral", "meh", "average", "normal"]
}

RISK_WEIGHTS = {
    "joy": "low",
    "neutral": "low",
    "surprise": "low",
    "sadness": "medium",
    "anger": "medium",
    "fear": "high",
    "stress": "high"
}

SENTIMENT_MAP = {
    "joy": "positive",
    "surprise": "positive",
    "neutral": "neutral",
    "sadness": "negative",
    "anger": "negative",
    "fear": "negative",
    "stress": "negative"
}

@app.get("/health")
def health():
    return {"status": "ok", "service": "MindCare AI Text Emotion Service"}

@app.post("/analyze/text", response_model=TextAnalysisResponse)
def analyze_text(request: TextAnalysisRequest):
    text = (request.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text field is required")

    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    token_set = set(tokens)

    scores = {emotion: 0 for emotion in EMOTION_LEXICON}
    for emotion, words in EMOTION_LEXICON.items():
        for word in words:
            if word in token_set or word in text.lower():
                scores[emotion] += 1

    primary_emotion = max(scores, key=lambda k: (scores[k], -len(k)))
    if scores[primary_emotion] == 0:
        primary_emotion = "neutral"

    sentiment = SENTIMENT_MAP.get(primary_emotion, "neutral")
    risk = RISK_WEIGHTS.get(primary_emotion, "low")
    confidence = min(98, max(55, 50 + scores[primary_emotion] * 12 + len(text) // 45))

    return {
        "source": "text",
        "text": text,
        "emotion": primary_emotion,
        "sentiment": sentiment,
        "risk": risk,
        "confidence": confidence,
        "scores": scores
    }
