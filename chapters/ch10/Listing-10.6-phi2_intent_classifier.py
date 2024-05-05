import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import warnings
import re
import logging
#from openai import OpenAI

DEBUG = True

warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", 
                                             torch_dtype="auto",
                                             trust_remote_code=True)

tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", 
                                          trust_remote_code=True)

# Set the default device to CUDA if available, otherwise use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Check if the question is about dogs
def check_dog_question(question):
    system_prompt = f"Instruct: Is there anything about dogs in the question below? If yes, answer with 'yes' else 'no'.\nQuestion:{question}\nOutput:"
    prompt = f"{system_prompt}\nUser:{question}\nOutput:"
    
    with torch.no_grad():
        inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=False, add_special_tokens=False)
        if DEBUG:
            print(f"Calling model with Inputs:{inputs}")
        inputs = {name: tensor.to(model.device) for name, tensor in inputs.items()}
        outputs = model.generate(**inputs, max_length=500, pad_token_id=tokenizer.eos_token_id)

    text = tokenizer.batch_decode(outputs)[0]
    # Remove the prompt from the output text
    text = text.replace(prompt, '').strip()
    text = text.replace("<|endoftext|>", '').strip()
    
    if DEBUG:
        print(f"Answer:{text}")
        
    regex = "^Output: Yes$"
    match = re.search(regex, text, re.MULTILINE)
    if match:
        if DEBUG:
            print("Found a match:", match.group())
        return True
    else:
        if DEBUG:
            print("No match found")
    
    return False

# Handle the user prompt
def handle_prompt(user_input)->str:
    prompt = f"Instruct: Tell me more about this:{user_input}\nOutput:"

    with torch.no_grad():
        inputs = tokenizer(prompt,
                           return_tensors="pt",
                           return_attention_mask=False,
                           add_special_tokens=False)
        inputs = {name: tensor.to(model.device) for name,
                  tensor in inputs.items()}
        outputs = model.generate(**inputs,
                                 max_length=500,
                                 pad_token_id=tokenizer.eos_token_id)
        
    text = tokenizer.batch_decode(outputs)[0]

    # Remove the prompt from the output text
    text = text.replace(prompt, '').strip()
    text = text.replace("<|endoftext|>", '').strip()
    
    return text

# Handle the dog question
def handle_dog_question(question):
    # Handle the question using RAG and GPT4
    # This is a placeholder function, replace it with your actual implementation
    
    # Call OpenAI's GPT-4 to answer the question
    # Implement openai call here
    openai_response = "Calling OpenAI's GPT-4 to answer the question: {question}"
    
    # openai.api_key = ""
    # openai_response = openai.Completion.create(
    #   engine="text-davinci-003",
    #   prompt=f"Ask a question about dogs: {question}",
    #   max_tokens=100
    # )
    
    # openai_response = "This is a response from RAG and GPT4"
    return openai_response
    
# Main function
if __name__=="__main__": 
    # Loop until the user enters "quit"
    while True:
        # Take user input
        user_prompt = input("What is your question (or type 'quit' to exit):")

        if user_prompt.casefold() == 'quit':
            break

        if check_dog_question(user_prompt):
            print(handle_dog_question(user_prompt))
        else:
            print("🤖 You did not ask about dogs")
            print("handle_prompt(user_prompt)")
    print("-" * 100)