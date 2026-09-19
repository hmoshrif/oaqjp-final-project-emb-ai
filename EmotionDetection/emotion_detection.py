"""Detect emotions with the Watson NLP service provided by Skills Network."""

import json
import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return five emotion scores and their dominant label, or None on HTTP 400."""
    if not isinstance(text_to_analyze, str):
        raise TypeError("text_to_analyze must be a string")
    response = requests.post(
        URL,
        json={"raw_document": {"text": text_to_analyze.strip()}},
        headers=HEADERS,
        timeout=30,
    )
    if response.status_code == 400:
        return dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    response.raise_for_status()
    payload = json.loads(response.text)
    scores = payload["emotionPredictions"][0]["emotion"]
    result = {name: scores[name] for name in EMOTIONS}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
