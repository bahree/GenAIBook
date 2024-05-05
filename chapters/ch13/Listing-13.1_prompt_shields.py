import os
import requests

# Set OpenAI API key
CONTENT_SAFETY_KEY = os.getenv("AOAI_KEY")
CONTENT_SAFETY_ENDPOINT = os.getenv("AOAI_ENDPOINT")
API_VERSION = "2024-02-15-preview"
DEBUG = True

# Build the request body
def shield_prompt_body(user_prompt: str,documents: list) -> dict:
    body = {
        "userPrompt": user_prompt,
        "documents": documents
    }
    return body

# Send the API request
def detect_groundness_result(data: dict, url: str):
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY
    }

    # Post the API request
    response = requests.post(url, headers=headers, json=data, timeout=10)
    return response

# Main code
if __name__ == "__main__":
    # Set according to the actual task category.
    user_prompt = "<test_user_prompt>"
    documents = [
        "<this_is_a_document>",
        "<this_is_another_document>"
    ]

    # Build the request body
    data = shield_prompt_body(user_prompt=user_prompt, documents=documents)
    
    # Set up the API request
    url = f"{CONTENT_SAFETY_ENDPOINT}/contentsafety/text:shieldPrompt?api-version={API_VERSION}"

    # Send the API request
    response = detect_groundness_result(data=data, url=url, subscription_key=CONTENT_SAFETY_KEY)

    # Handle the API response
    if response.status_code == 200:
        result = response.json()
        print("shieldPrompt result:", result)
    else:
        print("Error:", response.status_code, response.text)
