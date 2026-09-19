"""Run the five required examples against the real Watson service."""

import unittest
from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Verify the dominant emotion for each example in the lab guide."""

    def test_joy(self):
        """A glad statement should produce joy."""
        self.assertEqual(emotion_detector("I am glad this happened")["dominant_emotion"], "joy")

    def test_anger(self):
        """A mad statement should produce anger."""
        self.assertEqual(emotion_detector("I am really mad about this")["dominant_emotion"], "anger")

    def test_disgust(self):
        """A disgusted statement should produce disgust."""
        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result["dominant_emotion"], "disgust")

    def test_sadness(self):
        """A sad statement should produce sadness."""
        self.assertEqual(emotion_detector("I am so sad about this")["dominant_emotion"], "sadness")

    def test_fear(self):
        """An afraid statement should produce fear."""
        result = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result["dominant_emotion"], "fear")


if __name__ == "__main__":
    unittest.main(verbosity=2)
