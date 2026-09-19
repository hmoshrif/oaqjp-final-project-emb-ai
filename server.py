"""Serve the Emotion Detector user interface and Watson-backed predictions."""

from flask import Flask, render_template, request
from requests import RequestException
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Render the supplied application page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Analyze the submitted text and display scores or a helpful error."""
    text = request.args.get("textToAnalyze", "")
    try:
        result = emotion_detector(text)
    except (RequestException, ValueError, KeyError, IndexError, TypeError):
        app.logger.exception("Emotion service request failed")
        return "Emotion service is unavailable. Please try again later."
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"
    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
