# Listing: 1.1 - Basic Hello World example using the OpenAI API
import openai

gpt_model = "text-davinci-003"

# Replace with your actual OpenAI API key and organization ID
openai.api_key = 'your-api-key'
openai.organization = "your-organization-id-here"

# Generate English text
response_english = openai.Completion.create(
  engine=gpt_model,
  prompt="Hello, World!",
  max_tokens=50
)

print(response_english.choices[0].text.strip())  # This prints the completion of "Hello, World!"

# Translate English text to French
response_french = openai.Completion.create(
  engine=gpt_model,
  prompt=f'Translate the following English text to French: "{response_english.choices[0].text.strip()}"',
  max_tokens=60
)

print(response_french.choices[0].text.strip())  # This prints the translation to French
