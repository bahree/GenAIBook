# pip install google-api-python-client
import os
from googleapiclient import discovery
import json

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
SERVICE_URL = 'https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1'

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=GOOGLE_API_KEY,
  discoveryServiceUrl=SERVICE_URL,
  static_discovery=False,
)

analyze_request = {
  #'comment': { 'text': 'Hello World - Greetings from the GenAI Book!' },
  'comment': { 'text': 'What kind of an idiot name is foo for a function' },
  'requestedAttributes': {'TOXICITY': {},
                          'THREAT': {}},
}

response = client.comments().analyze(body=analyze_request).execute()
print(json.dumps(response, indent=2))