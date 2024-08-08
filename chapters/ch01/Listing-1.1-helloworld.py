# Listing: 1.1 - Basic Hello World example using the OpenAI API

import os
from openai import OpenAI

GPT_MODEL = "gpt-3.5-turbo"

# Replace with your actual OpenAI API key
client = OpenAI(api_key='your-api-key')

# Generate English text
response_english = client.chat.completions.create(
    model=GPT_MODEL,
    messages=[
      {
        "role": "user",
        "content": "Hello, World!"
      }
    ],
    max_tokens=50
)
english_text = response_english.choices[0].message.content.strip()
print(english_text)

# Translate English text to French
response_french = client.chat.completions.create(
    model=GPT_MODEL,
    
    messages=[
      {
        "role": "user",
        "content": "Translate the following English text to French: " + english_text
      }
    ],
    max_tokens=100
)
# This prints the translation to French
print(response_french.choices[0].message.content.strip())
