import os
import logging
import random
import time
from tqdm import tqdm
from openai import AzureOpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Set up logging
logging.basicConfig(filename='aoai_ptu.log', level=logging.INFO)

# Define constants
LOAD_TEST_ITERATIONS = 10

# Azure OpenAI Chat API endpoint and API key
AOAI_PTU_KEY = os.getenv("AOAI_PTU_KEY")
AOAI_PTU_ENDPOINT = os.getenv("AOAI_PTU_ENDPOINT")
API_VERSION = "2024-02-15-preview"
PTU_MODEL = "demo-sb"

AOAI_PAYGO_KEY = os.getenv("AOAI_KEY")
AOAI_PAYGO_ENDPOINT = os.getenv("AOAI_ENDPOINT")
PAYGO_MODEL = "gp4"

TEMPERATURE = 0.75
MAX_TOKENS = 256
NUM_INTERATION = 100
DEBUG = False

# Initialize Azure OpenAI clients
ptu_client = AzureOpenAI(azure_endpoint=AOAI_PTU_ENDPOINT,
                         api_key=AOAI_PTU_KEY,
                         api_version=API_VERSION)

paygo_client = AzureOpenAI(azure_endpoint=AOAI_PAYGO_ENDPOINT,
                           api_key=AOAI_PAYGO_KEY,
                           api_version=API_VERSION)

# Test inputs
test_inputs = ["Hello", "How are you?",
               "What's the capital of Hawaii?",
               "Tell me a dad joke",
                "Tell me a story",
                "What's your favorite movie?",
                "What's the meaning of life?",
                "What's the capital of India?",
                "What's the square root of 1976?",
                "What's the largest mammal?",
                "Write a story about a Panda F1 driver in less than {MAX_TOKENS} words"]

# Function to call the Azure OpenAI Chat API and measure latency
def call_completion_api(client, model, user_input):
    conversation = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": user_input}
    ]
    
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model=model,
            messages=conversation,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS)
        latency = time.time() - start_time
        
        message_response = response.choices[0].message.content
        token_count = response.usage.completion_tokens
        
        if DEBUG:
            logging.info("AI Assistant: %s", message_response)
        return latency, token_count
    except Exception as e:
        logging.error("Error calling API: %s", str(e))
        return None, None

# Main function to run the load test
def main():
    for client, model, test_name in [(ptu_client, PTU_MODEL, "PTU"), (paygo_client, PAYGO_MODEL, "PAYGO")]:
        print(f"Starting {test_name} test...")
        with ThreadPoolExecutor(max_workers=20) as executor:
            latencies = []
            futures = [executor.submit(call_completion_api, client, model, input) for input in random.choices(test_inputs, k=NUM_INTERATION)]
            for future in tqdm(as_completed(futures), total=NUM_INTERATION):
                latency, token_count = future.result()
                if latency is not None and token_count is not None:
                    logging.info(f"Latency: {latency}s, Token Count: {token_count}")
                    latencies.append(latency)
        
        # Calculate and print metrics
        average_latency = sum(latencies) / len(latencies) if latencies else None
        min_latency = min(latencies) if latencies else None
        max_latency = max(latencies) if latencies else None
        median_latency = statistics.median(latencies) if latencies else None
        
        print(f"Median Latency: {median_latency}s")
        print(f"Average Latency: {average_latency}s")
        print(f"Min Latency: {min_latency}s")
        print(f"Max Latency: {max_latency}s")
    
if __name__ == "__main__":
    main()