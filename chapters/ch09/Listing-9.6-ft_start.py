# Start the fine-tuning job

import os
from openai import AzureOpenAI

API_VERSION = '2023-09-15-preview'

client = AzureOpenAI(
    api_key=os.getenv('AOAI_FT_KEY'),
    api_version=API_VERSION,
    azure_endpoint = os.getenv('AOAI_FT_ENDPOINT'))

# Begin fine-tuning
# Training file ID: file-0678a7e63fca41a092cffcc473931da2
# Training file name: emoji_FT_train.jsonl

ft = client.fine_tuning.jobs.create(
    training_file="file-0678a7e63fca41a092cffcc473931da2",
    model="gpt-35-turbo-0613",
    hyperparameters={
        "n_epochs":3
    },
    suffix="emoji"
)
print("Finetuning job ID:", ft.id)

# Output:
# Finetuning job ID: ftjob-bfaadc862e2c4e66834925fbb645ba80

# List all the FT jobs
ft_jobs = client.fine_tuning.jobs.list()

for ft_job in ft_jobs:
    print(ft_job.id, ft_job.status)

# Output:
# ftjob-bfaadc862e2c4e66834925fbb645ba80 pending
# ftjob-367ee1995af740a0bf24876221585f7a succeeded
# ftjob-c41a9dc551834a1aa0be8befe788a22b succeeded
# ftjob-1a7faac8856d46e48a038c02555fe6e5 succeeded
# ftjob-505d5a8bd321406dbf4605b636b0c0cd succeeded
