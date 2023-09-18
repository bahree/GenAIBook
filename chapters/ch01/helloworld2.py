import requests
import json

# Replace with your GPT-4 API key
api_key = 'your_api_key_here'
url = 'https://api.openai.com/v1/engines/gpt-4/completions'

# Function to call GPT-4 API
def call_gpt4(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        'prompt': prompt,
        'max_tokens': 50,
        'n': 1,
        'stop': None,
        'temperature': 1.0
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_json = response.json()
        choices = response_json['choices']
        if choices:
            return choices[0]['text'].strip()
    else:
        print(f"Error: {response.status_code}")
        return None

# Main function to send "Hello, World!" prompt to GPT-4
def main():
    prompt = "Hello, World! Write a short message for the user."
    response_text = call_gpt4(prompt)
    
    if response_text:
        print(response_text)
    else:
        print("No response received from GPT-4.")

if __name__ == '__main__':
    main()
