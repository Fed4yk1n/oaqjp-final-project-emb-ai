"""Emotion analysis client for the Watson NLP service."""

import json
import requests


EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyse):
    """Return emotion scores and the dominant emotion for supplied text."""
    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(EMOTION_URL, json=payload, headers=headers, timeout=15)
    if response.status_code == 400:
        return {emotion: None for emotion in EMOTIONS} | {"dominant_emotion": None}

    response.raise_for_status()
    emotions = json.loads(response.text)["emotionPredictions"][0]["emotion"]
    return {emotion: emotions.get(emotion) for emotion in EMOTIONS} | {
        "dominant_emotion": max(EMOTIONS, key=lambda emotion: emotions.get(emotion, 0))
    }
