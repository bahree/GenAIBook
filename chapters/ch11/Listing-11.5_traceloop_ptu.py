# # pip install traceloop-sdk

# import os
# from openai import OpenAI
# from traceloop.sdk import Traceloop

# # Set OpenAI API key
# API_KEY = os.getenv("OPENAI_API_BOOK_KEY")
# MODEL = "gpt-3.5-turbo"
# TRACELOOP_API_KEY = os.getenv("TRACELOOP_API_KEY")
# TEMPERATURE = 0.7
# MODEL = "gpt-3.5-turbo"
# MAX_TOKENS = 256

# Traceloop.init(disable_batch=True,
#                app_name="GenAIBook_Chatbot",
#                api_key=TRACELOOP_API_KEY)

# #Traceloop.init(disable_batch=True)

# # Set your OpenAI API key
# client = OpenAI(api_key=API_KEY)

# # Define the conversation as a list of messages
# conversation = [
#     {"role": "system", "content": "You are a helpful assistant."},
# ]

# print("Type 'exit' to stop the conversation.")
# while True:
#     # Get user input
#     user_input = input("You: ")
#     if user_input.casefold() in ["exit", "quit", "q", "e"]:
#         break

#     # Add user input to the conversation
#     conversation.append({"role": "user", "content": user_input})

#     # Make the API call
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=conversation,
#         temperature=TEMPERATURE,
#         max_tokens=MAX_TOKENS
#     )

#     # Print the assistant's reply
#     print("AI Assistant:", response.choices[0].message.content)

import os
from traceloop.sdk import Traceloop
import logging
from tqdm import tqdm
import random
from openai import AzureOpenAI

# Set up logging
logging.basicConfig(filename='ptulogfile.log', level=logging.INFO)

# Define constants
MAX_TOKENS = 15
LOAD_TEST_ITERATIONS = 50
TEMPERATURE = 0.95
MODEL = "demo-sb"

# Set OpenAI API key
API_KEY = os.getenv("AOAI_PTU_KEY")
ENDPOINT = os.getenv("AOAI_PTU_ENDPOINT")
TRACELOOP_API_KEY = os.getenv("TRACELOOP_API_KEY")

# Initialize Traceloop
Traceloop.init(api_key=TRACELOOP_API_KEY)

client = AzureOpenAI(
    azure_endpoint = ENDPOINT,
    api_key=API_KEY,
    api_version="2024-02-15-preview"
)

# Define the conversation as a list of messages
conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
]

# Define a list of test inputs
test_inputs = ["Hello", "How are you?", "What's the weather like?", "Tell me a joke", "Tell me a story", "What's your favorite movie?", "What's the meaning of life?", "What's the capital of France?", "What's the square root of 144?", "What's the largest mammal?"]

print("Starting load test...")
for _ in tqdm(range(LOAD_TEST_ITERATIONS)):
    # Generate a random user input
    user_input = random.choice(test_inputs)

    # Add user input to the conversation
    conversation.append({"role": "user", "content": user_input})

    # Make the API call
    response = client.chat.completions.create(
        model=MODEL,
        messages=conversation,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    # Log the assistant's reply
    logging.info("AI Assistant: %s", response.choices[0].message.content)
print("Load test complete.")