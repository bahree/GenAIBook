# Upload fine-tuning files
import os
from openai import AzureOpenAI

API_VERSION = '2023-09-15-preview'

client = AzureOpenAI(
    api_key=os.getenv('AOAI_FT_KEY'),
    api_version=API_VERSION,
    azure_endpoint = os.getenv('AOAI_FT_ENDPOINT'))

TRAINING_FILENAME = 'data/emoji_FT_train.jsonl'
#validation_file_name = 'data/validation_set.jsonl'

# Upload the training and validation dataset files to Azure OpenAI with the SDK.
file = client.files.create(
    file=open(TRAINING_FILENAME, "rb"),
    purpose="fine-tune"
)

print("Training file ID:", file.id)
print("Training file name:", file.filename)
