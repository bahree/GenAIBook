import unittest
from unittest.mock import patch, MagicMock
import os
import openai

class TestOpenAICompletion(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.api_base = "test_api_base"
        os.environ["AOAI_KEY"] = self.api_key
        os.environ["AOAI_ENDPOINT"] = self.api_base

    @patch('openai.Completion.create')
    def test_completion_create(self, mock_create):
        mock_create.return_value = {
            "choices": [
                {"text": "test_text"}
            ]
        }
        prompt_startphrase = "Suggest three names for a new pet salon business."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_startphrase,
            temperature=0.8,
            max_tokens=100,
            suffix="\nThats all folks!",
            stop=None)
        self.assertEqual(response["choices"][0]["text"], "test_text")

    @patch('builtins.print')
    def test_print(self, mock_print):
        prompt_startphrase = "Suggest three names for a new pet salon business."
        responsetext = "test_text"
        print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
        mock_print.assert_called_with("Prompt:Suggest three names for a new pet salon business.\nResponse:test_text")

if __name__ == '__main__':
    unittest.main()