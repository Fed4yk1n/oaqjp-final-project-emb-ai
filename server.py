"""Flask web server for the Emotion Detector application."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector


app = Flask(__name__)


@app.route("/")
def index():
    """Render the input form."""
    return render_template("response.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze query text and render the result or a blank-input error."""
    text_to_analyse = request.args.get("textToAnalyze", "").strip()
    if not text_to_analyse:
        return "Please enter a text to analyze.", 400

    result = emotion_detector(text_to_analyse)
    return render_template("response.html", result=result, text=text_to_analyse)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
