import tiktoken as tk

def count_tokens(string: str, encoding_name: str) -> int:
    # Get the encoding
    encoding = tk.get_encoding(encoding_name)
    
    # Encode the string
    encoded_string = encoding.encode(string)

    # Count the number of tokens
    num_tokens = len(encoded_string)
    return num_tokens

# Define the input string
prompt = "I have a white dog named Champ"

# Display the number of tokens in the string
print("Number of tokens:" , count_tokens(prompt, "cl100k_base"))
