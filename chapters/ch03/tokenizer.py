import tiktoken as tk

def get_tokens(string: str) -> str:
    # Get the encoding
    encoding = tk.get_encoding("p50k_base")
    
    # Encode the string
    return encoding.encode(string)
  
# The array of text you want to count tokens in  
texts = ["Purr Purrs Meow Purr purr purrs meow"] 

for text in texts:  
    # Tokenize the text  
    tokenized_text = get_tokens(text)  
  
    # Print the original and tokenized text  
    print(f"'{text}:{tokenized_text}'")
