"""Check invalid responses and the web error message without network calls."""

import unittest
from unittest.mock import Mock, patch
from EmotionDetection.emotion_detection import EMOTIONS, emotion_detector
from server import app


class TestErrorHandling(unittest.TestCase):
    """Cover HTTP 400, invalid JSON and the browser-facing empty-input error."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_and_whitespace(self, post):
        """Whitespace is normalized and HTTP 400 maps every result field to None."""
        post.return_value = Mock(status_code=400)
        result = emotion_detector("   ")
        self.assertEqual(result, dict.fromkeys((*EMOTIONS, "dominant_emotion")))
        self.assertEqual(post.call_args.kwargs["json"]["raw_document"]["text"], "")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_malformed_service_response(self, post):
        """A non-JSON response cannot become a successful prediction."""
        post.return_value = Mock(status_code=200, text="not json")
        with self.assertRaises(ValueError):
            emotion_detector("Example")

    @patch("server.emotion_detector")
    def test_blank_input_web_message(self, detector):
        """The supplied frontend receives the required message with HTTP 200."""
        detector.return_value = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
        response = app.test_client().get("/emotionDetector", query_string={"textToAnalyze": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")


if __name__ == "__main__":
    unittest.main(verbosity=2)
