import tiktoken as tk

def get_tokens(string: str, encoding_name: str) -> str:
    # Get the encoding
    encoding = tk.get_encoding(encoding_name)
    
    # Encode the string
    return encoding.encode(string)

def get_string(tokens: str, encoding_name: str) -> str:
    # Get the encoding
    encoding = tk.get_encoding(encoding_name)
    
    # Decode the tokens
    return encoding.decode(tokens)


# Define the input string
prompt = "I have a white dog named Champ."

# Display the tokens
print("cl100k_base Tokens:" , get_tokens(prompt, "cl100k_base"))
print("  p50k_base Tokens:" , get_tokens(prompt, "p50k_base"))
print("  r50k_base Tokens:" , get_tokens(prompt, "r50k_base"))


# The original tokens: [40, 617, 264, 4251, 5679, 7086, 56690, 13]
print("Original String:" , get_string([40, 617, 264, 4251, 5679, 7086, 56690], "cl100k_base"))