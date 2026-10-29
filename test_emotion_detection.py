import json
import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    def mock_response(self, scores, status_code=200):
        response = Mock()
        response.status_code = status_code
        response.text = json.dumps({"emotionPredictions": [{"emotion": scores}]})
        response.raise_for_status.return_value = None
        return response

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_joy(self, post):
        post.return_value = self.mock_response(
            {"anger": 0.01, "disgust": 0.01, "fear": 0.01, "joy": 0.96, "sadness": 0.01}
        )
        self.assertEqual(emotion_detector("I am glad this happened")["dominant_emotion"], "joy")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_anger(self, post):
        post.return_value = self.mock_response(
            {"anger": 0.96, "disgust": 0.01, "fear": 0.01, "joy": 0.01, "sadness": 0.01}
        )
        self.assertEqual(emotion_detector("I am really mad about this")["dominant_emotion"], "anger")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_sadness(self, post):
        post.return_value = self.mock_response(
            {"anger": 0.01, "disgust": 0.01, "fear": 0.01, "joy": 0.01, "sadness": 0.96}
        )
        self.assertEqual(emotion_detector("I feel sad")["dominant_emotion"], "sadness")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_disgust(self, post):
        post.return_value = self.mock_response(
            {"anger": 0.01, "disgust": 0.96, "fear": 0.01, "joy": 0.01, "sadness": 0.01}
        )
        self.assertEqual(emotion_detector("That is disgusting")["dominant_emotion"], "disgust")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_fear(self, post):
        post.return_value = self.mock_response(
            {"anger": 0.01, "disgust": 0.01, "fear": 0.96, "joy": 0.01, "sadness": 0.01}
        )
        self.assertEqual(emotion_detector("I am afraid")["dominant_emotion"], "fear")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_bad_request(self, post):
        post.return_value = self.mock_response({}, status_code=400)
        result = emotion_detector("")
        self.assertIsNone(result["dominant_emotion"])
        self.assertTrue(all(result[emotion] is None for emotion in ("anger", "disgust", "fear", "joy", "sadness")))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_output_format(self, post):
        post.return_value = self.mock_response(
            {"anger": 0.01, "disgust": 0.01, "fear": 0.01, "joy": 0.96, "sadness": 0.01}
        )
        self.assertEqual(
            set(emotion_detector("I am happy")),
            {"anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"},
        )


if __name__ == "__main__":
    unittest.main()