# Polling for to check a fine-tuning job events

import os
import time
from openai import AzureOpenAI
from IPython.display import clear_output

# Define the API version
API_VERSION = '2023-09-15-preview'

# Create an instance of the AzureOpenAI client
client = AzureOpenAI(
    api_key=os.getenv('AOAI_FT_KEY'),
    api_version=API_VERSION,
    azure_endpoint = os.getenv('AOAI_FT_ENDPOINT'))

# Define the job ID of the fine-tuning job to track
JOB_ID = "ftjob-bfaadc862e2c4e66834925fbb645ba80"

# Record the start time of the tracking
start_time = time.time()

# Get the status of our fine-tuning job.
ft_job = client.fine_tuning.jobs.retrieve(JOB_ID)
status = ft_job.status

# If the job isn't done yet, poll it every 30 seconds.
while status not in ["succeeded", "failed"]:
    ft_job = client.fine_tuning.jobs.retrieve(JOB_ID)
    print(ft_job)
    status = ft_job.status
    print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))
    print(f'Status: {status}')

    clear_output(wait=True)
    time.sleep(30)
   
print(f'Fine-tuning job {JOB_ID} finished with status: {status}')
