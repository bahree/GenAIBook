import os
import sys
import openai

openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_ENDPOINT")
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("AOAI_KEY")

prompt_startphrase = "Suggest three names for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

for response in openai.Completion.create(
  engine="text-davinci-003",
  prompt=prompt_startphrase,
  temperature=0.8,
  max_tokens=500,
  n=1,
  stream=True,
  stop=None):
    for choice in response.choices:
        #sys.stdout.write(choice.text)
        sys.stdout.write(str(choice)+"\n")
        sys.stdout.flush()
    

import unittest
from unittest.mock import patch, Mock
import sys
import openai

class TestStream(unittest.TestCase):
    
    @patch('sys.stdout', new_callable=Mock)
    def test_stream_output(self, mock_stdout):
        # Arrange
        prompt_startphrase = "The quick brown fox"
        mock_response = Mock()
        mock_response.choices = [{'text': ' jumps over the lazy dog.'}]
        openai.Completion.create.return_value = mock_response
        
        # Act
        for response in openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_startphrase,
            temperature=0.8,
            max_tokens=500,
            n=1,
            stream=True,
            stop=None):
            for choice in response.choices:
                sys.stdout.write(choice.text)
                sys.stdout.flush()
        
        # Assert
        mock_stdout.write.assert_called_once_with(' jumps over the lazy dog.')
        
    def test_stream_parameters(self):
        # Arrange
        prompt_startphrase = "The quick brown fox"
        
        # Act
        for response in openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_startphrase,
            temperature=0.8,
            max_tokens=500,
            n=1,
            stream=True,
            stop=None):
            pass
        
        # Assert
        openai.Completion.create.assert_called_once_with(
            engine="text-davinci-003",
            prompt=prompt_startphrase,
            temperature=0.8,
            max_tokens=500,
            n=1,
            stream=True,
            stop=None
        )
        
    def test_stream_stop(self):
        # Arrange
        prompt_startphrase = "The quick brown fox"
        
        # Act
        for response in openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_startphrase,
            temperature=0.8,
            max_tokens=500,
            n=1,
            stream=True,
            stop="stop"
        ):
            pass
        
        # Assert
        openai.Completion.create.assert_called_once_with(
            engine="text-davinci-003",
            prompt=prompt_startphrase,
            temperature=0.8,
            max_tokens=500,
            n=1,
            stream=True,
            stop="stop"
        )
        
if __name__ == '__main__':
    unittest.main()