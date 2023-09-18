import os
import openai

openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_ENDPOINT")
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("AOAI_KEY")
  
prompt_startphrase = "Suggest three names for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

response = openai.Completion.create(  
  engine="text-davinci-003",  
  prompt=prompt_startphrase,  
  temperature=0.8,  
  max_tokens=100,  
  logit_bias={
      30026:-100,
      81:-100,
      9330:-100,
      808:-100,
      42114:-100,
      1308:-100, 
      3808:-100,
      502:-100,
      322:-100,
      37:5,
      16682:5
  }  
)  
  
responsetext = response["choices"][0]["text"]

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)

print(response)
