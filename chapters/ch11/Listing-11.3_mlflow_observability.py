import os
import time
# import prometheus_client as prom
import mlflow
from openai import OpenAI
import tiktoken as tk
from colorama import Fore, Style, init

# Set OpenAI API key
API_KEY = os.getenv("OPENAI_API_BOOK_KEY")
MODEL = "gpt-3.5-turbo"
MLFLOW_URI = "http://localhost:5000"
TEMPERATURE = 0.7
TOP_P = 1
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0
MAX_TOKENS = 800
DEBUG = False

# Initialize colorama
init()

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Set MLflow tracking URI
mlflow.set_tracking_uri(MLFLOW_URI)
mlflow.set_experiment("GenAI_book")  # Replace with your experiment name

# Create Prometheus metrics
# REQUEST_COUNT = prom.Counter("openai_request_count", "Number of OpenAI API requests")
# REQUEST_LATENCY = prom.Histogram("openai_request_latency_seconds", "Latency of OpenAI API requests")

# Print user input and AI output with colors
def print_user_input(text):
    print(f"{Fore.GREEN}You: {Style.RESET_ALL}", text)

def print_ai_output(text):
    print(f"{Fore.BLUE}AI Assistant:{Style.RESET_ALL}", text)

# count tokens
def count_tokens(string: str, encoding_name="cl100k_base") -> int:
    # Get the encoding
    encoding = tk.get_encoding(encoding_name)
    
    # Encode the string
    encoded_string = encoding.encode(string, disallowed_special=())

    # Count the number of tokens
    num_tokens = len(encoded_string)
    return num_tokens

def generate_text(conversation, max_tokens=100)->str:
    # Generate text using OpenAI API
    start_time = time.time()
    response = client.chat.completions.create(
        model=MODEL,
        messages=conversation,
        temperature=TEMPERATURE,
        max_tokens=max_tokens,
        top_p=TOP_P,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY
    )
    latency = time.time() - start_time
    message_response = response.choices[0].message.content
    
    # Count tokens in the prompt and the completion
    prompt_tokens = count_tokens(conversation[-1]['content'])
    conversation_tokens = count_tokens(str(conversation))
    completion_tokens = count_tokens(message_response)
    
    # # Log metrics using MLflow
    # with mlflow.start_run():
    #     mlflow.log_metrics({
    #         "request_count": 1,
    #         "request_latency": latency,
    #         "prompt_tokens": prompt_tokens,
    #         "completion_tokens": completion_tokens,
    #         "conversation_tokens": conversation_tokens
    #         })
    #     mlflow.log_params({
    #         "model": MODEL,
    #         "temperature": TEMPERATURE,
    #         "top_p": TOP_P,
    #         "frequency_penalty": FREQUENCY_PENALTY,
    #         "presence_penalty": PRESENCE_PENALTY
    #         })
    
    run = mlflow.active_run()
    if DEBUG:    
        print(f"Run ID: {run.info.run_id}")
        input("Press Enter to continue...")

    mlflow.log_metrics({
        "request_count": 1,
        "request_latency": latency,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "conversation_tokens": conversation_tokens
    })
    
    mlflow.log_params({
        "model": MODEL,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "frequency_penalty": FREQUENCY_PENALTY,
        "presence_penalty": PRESENCE_PENALTY
    })

    
    # Expose metrics using Prometheus
    # REQUEST_COUNT.inc()
    # REQUEST_LATENCY.observe(latency)

    return message_response
        
if __name__ == "__main__":
    mlflow.autolog()

    # Start a new MLflow run
    with mlflow.start_run() as run:
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]

        while True:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit", "q", "e"]:
                break

            conversation.append({"role": "user", "content": user_input})
            ai_output = generate_text(conversation, MAX_TOKENS)
            print_ai_output(ai_output)
            conversation.append({"role": "assistant", "content": ai_output})