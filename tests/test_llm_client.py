import json
import unittest
from unittest.mock import patch

from note_generator.llm.llm_client import generate


class _FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


class LlmClientTests(unittest.TestCase):
    def test_generate_uses_lm_studio_chat_completions_shape(self) -> None:
        fake_response = _FakeResponse({"choices": [{"message": {"content": "Risposta di test"}}]})

        with patch("note_generator.llm.llm_client.request.urlopen", return_value=fake_response) as mock_urlopen:
            output = generate(
                "Ciao",
                model="test-model",
                base_url="http://localhost:1234/v1",
                api_key="secret",
                system_prompt="System prompt di test",
                temperature=0.2,
                max_tokens=12,
            )

        self.assertEqual(output, "Risposta di test")
        self.assertGreaterEqual(mock_urlopen.call_count, 1)

        request_object = mock_urlopen.call_args.args[0]
        self.assertEqual(request_object.full_url, "http://localhost:1234/v1/chat/completions")
        self.assertEqual(request_object.headers.get("Authorization"), "Bearer secret")

        payload = json.loads(request_object.data.decode("utf-8"))
        self.assertEqual(payload["model"], "test-model")
        self.assertEqual(payload["messages"][0]["role"], "system")
        self.assertEqual(payload["messages"][1]["content"], "Ciao")
        self.assertEqual(payload["temperature"], 0.2)
        self.assertEqual(payload["max_tokens"], 12)
        self.assertFalse(payload["stream"])


if __name__ == "__main__":
    unittest.main()