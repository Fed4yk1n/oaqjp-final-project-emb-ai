"""Flask web server for the Emotion Detector application."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector


app = Flask(__name__)


@app.route("/")
def index():
    """Render the input form."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze query text and render the result or a blank-input error."""
    text_to_analyse = request.args.get("textToAnalyze", "").strip()
    result = emotion_detector(text_to_analyse)
    if result["dominant_emotion"] is None:
        return "Invalid Input! Please try again."

    response_text = (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']}, 'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return response_text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
