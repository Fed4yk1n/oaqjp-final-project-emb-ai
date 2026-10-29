"""Emotion analysis client for the Watson NLP service."""

import requests


EMOTION_URL = "https://sn-watson-emotion.labs.skills.network/emotionAnalyses"
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyse):
    """Return emotion scores and the dominant emotion for supplied text."""
    response = requests.post(EMOTION_URL, json={"text": text_to_analyse}, timeout=15)
    if response.status_code == 400:
        return {emotion: None for emotion in EMOTIONS} | {"dominant_emotion": None}

    response.raise_for_status()
    emotions = response.json()
    emotions["dominant_emotion"] = max(
        EMOTIONS, key=lambda emotion: emotions.get(emotion, 0)
    )
    return {emotion: emotions.get(emotion) for emotion in EMOTIONS} | {
        "dominant_emotion": emotions["dominant_emotion"]
    }
