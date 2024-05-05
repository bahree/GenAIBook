# Listing: 1.1 - Basic Hello World example using the OpenAI API

import os
from openai import OpenAI

gpt_model = "gpt-3.5-turbo"

# Replace with your actual OpenAI API key
client = OpenAI(api_key='your-api-key')

# Generate English text
response_english = client.chat.completions.create(
    model="gpt-3.5-turbo",
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
    model="gpt-3.5-turbo",
    
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


#===================
# This is using the old OpenAI SDK version 0.28.0
# # Listing: 1.1 - Basic Hello World example using the OpenAI API

# import openai

# gpt_model = "text-davinci-003"

# # Replace with your actual OpenAI API key and organization ID
# openai.api_key = 'your-api-key'
# openai.organization = "your-organization-id-here"

# # Generate English text
# response_english = openai.Completion.create(
#   engine=gpt_model,
#   prompt="Hello, World!",
#   max_tokens=50
# )

# print(response_english.choices[0].text.strip())  # This prints the completion of "Hello, World!"

# # Translate English text to French
# response_french = openai.Completion.create(
#   engine=gpt_model,
#   prompt=f'Translate the following English text to French: "{response_english.choices[0].text.strip()}"',
#   max_tokens=60
# )

# print(response_french.choices[0].text.strip())  # This prints the translation to French

