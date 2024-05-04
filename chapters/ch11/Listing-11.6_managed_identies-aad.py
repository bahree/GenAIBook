import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Set your OpenAI API key
AOAI_API_KEY = os.getenv("AOAI_KEY")
AZURE_ENDPOINT = os.getenv("AOAI_ENDPOINT")
API_VERSION = "2024-02-15-preview"

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
    azure_ad_token_provider=token_provider,
)