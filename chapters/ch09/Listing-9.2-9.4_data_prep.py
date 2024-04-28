import json
from collections import defaultdict

import numpy as np
import tiktoken  # for token counting

data_file = "data/emoji_ft_train.jsonl"

encoding = tiktoken.get_encoding("cl100k_base")

# Pricing and default n_epochs estimate
MAX_TOKENS = 4096

TARGET_EPOCHS = 3
MIN_TARGET_EXAMPLES = 100
MAX_TARGET_EXAMPLES = 25000
MIN_DEFAULT_EPOCHS = 1
MAX_DEFAULT_EPOCHS = 25

# Estimate the number of tokens that will be charged for during training
def estimate_tokens(dataset, assistant_tokens):
    # Set the initial number of epochs to the target epochs
    n_epochs = TARGET_EPOCHS

    # Get the number of examples in the dataset
    n_train_examples = len(dataset)

    # If the examples total is less than the minimum target
    # adjust the epochs to ensure we have enough examples for
    # training
    if n_train_examples * TARGET_EPOCHS < MIN_TARGET_EXAMPLES:
        n_epochs = min(MAX_DEFAULT_EPOCHS, MIN_TARGET_EXAMPLES // n_train_examples)
    
    # If the  number of examples is more than the maximum target
    # adjust the  epochs to ensure we don't exceed the maximum 
    # for training
    elif n_train_examples * TARGET_EPOCHS > MAX_TARGET_EXAMPLES:
        n_epochs = max(MIN_DEFAULT_EPOCHS, MAX_TARGET_EXAMPLES // n_train_examples)

    # Calculate the total number of tokens in the dataset
    n_billing_tokens_in_dataset = sum(min(MAX_TOKENS, length) for length in assistant_tokens)

    # Print the total token count that will be charged during training
    print(f"Dataset has ~{n_billing_tokens_in_dataset} tokens that will be charged for during training")

    # Print the default number of epochs for training
    print(f"You will train for {n_epochs} epochs on this dataset")

    # Print the total number of tokens that will be charged during training
    print(f"You will be charged for ~{n_epochs * n_billing_tokens_in_dataset} tokens")

    # If the total token count exceeds the maximum tokens, print a warning 
    if n_billing_tokens_in_dataset > MAX_TOKENS:
        print(f"WARNING: Your dataset contains examples longer than 4K tokens by {n_billing_tokens_in_dataset - MAX_TOKENS} tokens.")
        print("You will be charged for the full length of these examples during training, but only the first 4K tokens will be used for training.")

# Print the number of tokens in the messages
def num_tokens_from_messages(messages, tokens_per_message=3, tokens_per_name=1):
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens

# print the number of tokens in the assistant messages
def num_assistant_tokens_from_messages(messages):
    num_tokens = 0
    for message in messages:
        if message["role"] == "assistant":
            num_tokens += len(encoding.encode(message["content"]))
    return num_tokens

# Print the distribution of values
def print_distribution(values, name):
    print(f"\n#### Distribution of {name}:")
    print(f"min / max: {min(values)}, {max(values)}")
    print(f"mean / median: {np.mean(values)}, {np.median(values)}")
    print(f"p5 / p95: {np.quantile(values, 0.1)}, {np.quantile(values, 0.9)}")

# Basic checks to ensure the data file is valid
def basic_checks(data_file):
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            dataset = [json.loads(line) for line in f]

        print(f"Basic checks for file {data_file}:")
        print("Count of examples in training dataset:", len(dataset))
        print("First example:")
        for message in dataset[0]["messages"]:
            print(message)
        return True
    except FileNotFoundError as e:
        print(f"File not found error occurred in file {data_file}: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"JSON decoding error occurred in file {data_file}: {e}")
        return False
    except Exception as e:
        print(f"An error occurred in file {data_file}: {e}")
        return False


# Checkthe data file format meets the chat format
# This function is not exhaustive, but it will catch most errors
def format_checks(dataset, filename):
    # Initialize a dictionary, used to track format errors
    format_errors = defaultdict(int)

    # Iterate over each example in the dataset
    for ex in dataset:
        # Check if the example is a dictionary, if not 
        # increment the corresponding error count
        if not isinstance(ex, dict):
            format_errors["data_type"] += 1
            continue

        # Check if the example has a "messages" key, 
        # if not increment the corresponding error count
        messages = ex.get("messages", None)
        if not messages:
            format_errors["missing_messages_list"] += 1
            continue

        # Iterate over each message in the messages list
        for message in messages:
            # Check if the message has "role" and "content" keys,
            # if not increment the corresponding error count
            if "role" not in message or "content" not in message:
                format_errors["message_missing_key"] += 1

            # Check if the message has any unrecognized keys,
            # if so increment the corresponding error count
            if any(k not in ("role", "content", "name", "function_call") for k in message):
                format_errors["message_unrecognized_key"] += 1

            # Check if the role of the message is one of the recognized
            # roles, if not increment the corresponding error count
            if message.get("role", None) not in (
                "system",
                "user",
                "assistant",
                "function",
            ):
                format_errors["unrecognized_role"] += 1

            # Check if the message has either content or a function call,
            # and if the content is a string, if not increment the
            # corresponding error count
            content = message.get("content", None)
            function_call = message.get("function_call", None)
            if (not content and not function_call) or not isinstance(content, str):
                format_errors["missing_content"] += 1

        # Check if there is at least one message with the role "assistant",
        # if not increment the corresponding error count
        if not any(message.get("role", None) == "assistant" for message in messages):
            format_errors["example_missing_assistant_message"] += 1

    # If there are any format errors, print them and return False
    if format_errors:
        print(f"Formatting errors found in file {filename}:")
        for k, v in format_errors.items():
            print(f"{k}: {v}")
        return False
    print(f"No formatting errors found in file {filename}")
    return True

# Main
if __name__ == "__main__":
    # files = ['training_set.jsonl', 'validation_set.jsonl']
    files = ["data/emoji_ft_train.jsonl", "data/emoji_ft_validation.jsonl"]

    for file in files:
        # Run basic checks on the data file
        if not basic_checks(file):
            print("Exiting...")
            exit()

    # input("Press Enter to continue...")
    print("-" * 50)

    # Now run additional checks for validate the token counts and the number of examples per label
    encoding = tiktoken.get_encoding("cl100k_base")

    # files = [f'data/emoji_ft_train.jsonl', f'data/emoji_ft_validation.jsonl']
    files = [
        "data/emoji_ft_train.jsonl",
        "data/emoji_ft_validation.jsonl",
        "data/dog_emoji_FT_train_large.jsonl",
    ]

    for file in files:
        print(f"Processing file: {file}")
        with open(file, "r", encoding="utf-8") as f:
            dataset = [json.loads(line) for line in f]

        total_tokens = []
        assistant_tokens = []

        if not format_checks(dataset, file):
            print("Exiting...")
            exit()

        for ex in dataset:
            messages = ex.get("messages", {})
            total_tokens.append(num_tokens_from_messages(messages))
            assistant_tokens.append(num_assistant_tokens_from_messages(messages))

        print_distribution(total_tokens, "total tokens")
        print_distribution(assistant_tokens, "assistant tokens")
        estimate_tokens(dataset, assistant_tokens)
        print(f"Processing file completed: {file}")
        print("-" * 50)
