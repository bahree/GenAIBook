# List all the events for a specific fine-tuning job

import os
from openai import AzureOpenAI

API_VERSION = '2023-09-15-preview'

client = AzureOpenAI(
    api_key=os.getenv('AOAI_FT_KEY'),
    api_version=API_VERSION,
    azure_endpoint = os.getenv('AOAI_FT_ENDPOINT'))

#List all the FT events for the job from earier - ftjob-bfaadc862e2c4e66834925fbb645ba80
ft_job_events = client.fine_tuning.jobs.list_events(
    fine_tuning_job_id="ftjob-bfaadc862e2c4e66834925fbb645ba80", 
    limit=10)

# Loop through the events and print the details
for ft_job_event in ft_job_events:
    print(ft_job_event.id, ft_job_event.message)