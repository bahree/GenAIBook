import http.client
import json

# Set the API endpoint and key
CONTENT_SAFETY_ENDPOINT = "https://demorai.cognitiveservices.azure.com/"
CONTENT_SAFETY_KEY = "your-api-key-here"
connection = http.client.HTTPSConnection(CONTENT_SAFETY_ENDPOINT)

# Build the request payload
payload = json.dumps({
    "domain": "Medical",
    "task": "Summarization",
    "text": "Ms Johnson has been in the hospital after experiencing a stroke.",
    "groundingSources": ["Our patient, Ms. Johnson, presented with persistent fatigue, unexplained weight loss, and frequent night sweats. After a series of tests, she was diagnosed with Hodgkin’s lymphoma, a type of cancer that affects the lymphatic system. The diagnosis was confirmed through a lymph node biopsy revealing the presence of Reed-Sternberg cells, a characteristic of this disease. She was further staged using PET-CT scans. Her treatment plan includes chemotherapy and possibly radiation therapy, depending on her response to treatment. The medical team remains optimistic about her prognosis given the high cure rate of Hodgkin’s lymphoma."],
    "reasoning": false
})

headers = {
  'Ocp-Apim-Subscription-Key': '{CONTENT_SAFETY_KEY}',
  'Content-Type': 'application/json'
}

# Send the API request
connection.request("POST", "/contentsafety/text:detectGroundedness?api-version=2024-02-15-preview", payload, headers)
res = connection.getresponse()
data = res.read()

print(data.decode("utf-8"))