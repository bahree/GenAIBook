import openai

# function to read the key
def read_api_key(file_path: str) -> str:
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

# Setup the OpenAI API key and organization
api_key_file = 'OPENAI_API_BOOK_KEY.key'
openai.organization = "your-organization-id-here"
openai.api_key = read_api_key(api_key_file)

# Set up the prompt for the model to generate "Hello, world!"
prompt = "Generate the text 'Hello, world!'"

# Set up the parameters for the GPT-3 model
model_engine = "gpt-4-0314"
max_tokens = 500

# Call the Completion API to generate the text
response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=max_tokens
)

# Print out the generated text
print(response.choices[0].text.strip())
