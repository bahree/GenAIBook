import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # Import tqdm
import statistics

# Azure OpenAI Chat API endpoint and API key
AOAI_API_KEY = os.getenv("AOAI_KEY")
ENDPOINT = os.getenv("AOAI_ENDPOINT")
MODEL = "gpt35"  # Model/Deployment name
API_VERSION = "2024-02-15-preview"

AZURE_ENDPOINT = f"{ENDPOINT}openai/deployments/{MODEL}/chat/completions?api-version={API_VERSION}"

DEBUG = True

# Number of requests to simulate
NUM_INTERATION = 100

headers = {
    "api-key": AOAI_API_KEY,
    "Content-Type": "application/json"
}

if DEBUG:
    print("Azure OpenAI Endpoint:", AZURE_ENDPOINT)
    print(headers)
    input("Press Enter to continue...")

# Define the payload, including the model to use
def get_payload():
    return {
        "model": MODEL,  # Specify the model here
        "max_tokens": 50,  # Adjust as needed
        "messages": [{"role": "system", "content": "You are a helpful assistant."}, 
                     {"role": "user", "content": "Hello, world!"}],
        "temperature": 0.95,
        "stream": True
    }

# Function to call the Azure OpenAI Chat API and measure latency
def call_api_and_measure_latency():
    payload = get_payload()
    start_time = time.time()
    response = requests.post(AZURE_ENDPOINT, headers=headers, json=payload, timeout=20)
    latency = time.time() - start_time
    return latency, response.status_code

def main():
    # Use ThreadPoolExecutor to simulate concurrent API calls
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(call_api_and_measure_latency) for _ in range(NUM_INTERATION)]
        latencies = []
        # Wrap as_completed(futures) with tqdm
        for future in tqdm(as_completed(futures), total=NUM_INTERATION):
            latency, status_code = future.result()
            print(f"Latency: {latency}s, Status Code: {status_code}")
            latencies.append(latency)

    # Calculate and print metrics
    average_latency = sum(latencies) / len(latencies)
    min_latency = min(latencies) if latencies else None
    max_latency = max(latencies) if latencies else None
    median_latency = statistics.median(latencies) if latencies else None
    
    print(f"Median Latency: {median_latency}s")
    print(f"Average Latency: {average_latency}s")
    print(f"Min Latency: {min_latency}s")
    print(f"Max Latency: {max_latency}s")
    
if __name__ == "__main__":
    main()