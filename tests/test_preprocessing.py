import unittest

from note_generator.preprocessing.cleaner import clean_transcription


class CleanTranscriptionTests(unittest.TestCase):
    def test_clean_transcription_removes_fillers_and_normalizes_math(self) -> None:
        result = clean_transcription("ok allora 3 per 5 x 2. Il sistema è affidabile.")

        self.assertNotIn("ok", result["cleaned_text"].lower())
        self.assertNotIn("allora", result["cleaned_text"].lower())
        self.assertIn("3 * 5 * 2", result["cleaned_text"])
        self.assertEqual(result["sentences"], ["3 * 5 * 2.", "Il sistema è affidabile."])


if __name__ == "__main__":
    unittest.main()
