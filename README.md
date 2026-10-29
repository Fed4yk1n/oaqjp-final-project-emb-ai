# Final Project

Emotion Detector is a Flask web application that uses the Watson NLP emotion
analysis service to classify text into anger, disgust, fear, joy, and sadness.

## Run

```bash
python3 -m pip install -r requirements.txt
python3 server.py
```

Open `http://localhost:5000` and submit text for analysis.

## Test and analyze

```bash
python3 test_emotion_detection.py
pylint server.py
```