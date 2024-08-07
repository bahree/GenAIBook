import requests
import os
from dotenv import load_dotenv

# Set the API endpoint and key
CONTENT_SAFETY_KEY = os.getenv("CONTENT_SAFETY_KEY")
CONTENT_SAFETY_ENDPOINT = os.getenv("CONTENT_SAFETY_ENDPOINT")
API_VERSION = "2024-02-15-preview"

# Build the request payload
payload = {
    "domain": "Medical",
    "task": "Summarization",
    "text": "Ms Johnson has been in the hospital after experiencing a stroke.",
    "groundingSources": ["Our patient, Ms. Johnson, presented with persistent fatigue, unexplained weight loss, and frequent night sweats. After a series of tests, she was diagnosed with Hodgkin’s lymphoma, a type of cancer that affects the lymphatic system. The diagnosis was confirmed through a lymph node biopsy revealing the presence of Reed-Sternberg cells, a characteristic of this disease. She was further staged using PET-CT scans. Her treatment plan includes chemotherapy and possibly radiation therapy, depending on her response to treatment. The medical team remains optimistic about her prognosis given the high cure rate of Hodgkin’s lymphoma."],
    "reasoning": False
}

headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY
}

# Send the API request
url = f"{CONTENT_SAFETY_ENDPOINT}/contentsafety/text:detectGroundedness?api-version={API_VERSION}"
response = requests.post(url, headers=headers, json=payload, timeout=10)

if response.status_code == 200:
    result = response.json()
    print("detectGroundedness result:", result)
else:
    print("Error:", response.status_code, response.text)
