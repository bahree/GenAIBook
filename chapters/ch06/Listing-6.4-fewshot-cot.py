import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY")
)

GPT_MODEL = "gpt-35-turbo"

# Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done,
# there will be 21 trees. How many trees did the grove workers plant today?
# A: We start with 15 trees. Later we have 21 trees. The difference must be the number of trees they planted.
# So, they must have planted 21 - 15 = 6 trees. The answer is 6.
# Q: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?
# A: There are 3 cars in the parking lot already. 2 more arrive. Now there are 3 + 2 = 5 cars. The answer is 5.
# Q: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?
# A: Leah had 32 chocolates and Leah’s sister had 42. That means there were originally 32 + 42 = 74
# chocolates. 35 have been eaten. So in total they still have 74 - 35 = 39 chocolates. The answer is 39.
# Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops
# did Jason give to Denny?
# A: Jason had 20 lollipops. Since he only has 12 now, he must have given the rest to Denny. The number of
# lollipops he has given to Denny must have been 20 - 12 = 8 lollipops. The answer is 8.
# Q: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does
# he have now?
# A: He has 5 toys. He got 2 from mom, so after that he has 5 + 2 = 7 toys. Then he got 2 more from dad, so
# in total he has 7 + 2 = 9 toys. The answer is 9.
# Q: There were nine computers in the server room. Five more computers were installed each day, from
# monday to thursday. How many computers are now in the server room?
# A: There are 4 days from monday to thursday. 5 computers were added each day. That means in total 4 * 5 =
# 20 computers were added. There were 9 computers in the beginning, so now there are 9 + 20 = 29 computers.
# The answer is 29.
# Q: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many
# golf balls did he have at the end of wednesday?
# A: Michael initially had 58 balls. He lost 23 on Tuesday, so after that he has 58 - 23 = 35 balls. On
# Wednesday he lost 2 more so now he has 35 - 2 = 33 balls. The answer is 33.
# Q: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?
# A: She bought 5 bagels for $3 each. This means she spent $15. She has $8 left.
# Q: When I was 6 my sister was half my age. Now I’m 70 how old is my sister?
# A:

# Q: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many
# golf balls did he have at the end of wednesday?
# A: Michael initially had 58 balls. He lost 23 on Tuesday, so after that he has 58 - 23 = 35 balls. On
# Wednesday he lost 2 more so now he has 35 - 2 = 33 balls. The answer is 33.
# Q: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?
# A: She bought 5 bagels for $3 each. This means she spent $15. She has $8 left.
# Q: When I was 6 my sister was half my age. Now I'm 70 how old is my sister?
# A:
# Response: When you were 6, your sister was half your age, so she was 3 years old. Now you are 70 so she is 70 - 3 = 67 years old. The answer is 67.


prompt_startphrase = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done,\nthere will be 21 trees. How many trees did the grove workers plant today?\nA: We start with 15 trees. Later we have 21 trees. The difference must be the number of trees they planted.\nSo, they must have planted 21 - 15 = 6 trees. The answer is 6.\nQ: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?\nA: There are 3 cars in the parking lot already. 2 more arrive. Now there are 3 + 2 = 5 cars. The answer is 5.\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?\nA: Leah had 32 chocolates and Leah’s sister had 42. That means there were originally 32 + 42 = 74\nchocolates. 35 have been eaten. So in total they still have 74 - 35 = 39 chocolates. The answer is 39.\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops\ndid Jason give to Denny?\nA: Jason had 20 lollipops. Since he only has 12 now, he must have given the rest to Denny. The number of\nlollipops he has given to Denny must have been 20 - 12 = 8 lollipops. The answer is 8.\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does\nhe have now?\nA: He has 5 toys. He got 2 from mom, so after that he has 5 + 2 = 7 toys. Then he got 2 more from dad, so\nin total he has 7 + 2 = 9 toys. The answer is 9.\nQ: There were nine computers in the server room. Five more computers were installed each day, from\nmonday to thursday. How many computers are now in the server room?\nA: There are 4 days from monday to thursday. 5 computers were added each day. That means in total 4 * 5 =\n20 computers were added. There were 9 computers in the beginning, so now there are 9 + 20 = 29 computers.\nThe answer is 29.\nQ: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many\ngolf balls did he have at the end of wednesday?\nA: Michael initially had 58 balls. He lost 23 on Tuesday, so after that he has 58 - 23 = 35 balls. On\nWednesday he lost 2 more so now he has 35 - 2 = 33 balls. The answer is 33.\nQ: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?\nA: She bought 5 bagels for $3 each. This means she spent $15. She has $8 left.\nQ: When I was 6 my sister was half my age. Now I'm 70 how old is my sister?\nA:"

response = client.completions.create(
    model=GPT_MODEL,
    prompt=prompt_startphrase,
    temperature=0.8,
    max_tokens=100,
    stop=None)

#responsetext = response["choices"][0]["text"]
responsetext = response.choices[0].text

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)

#print(response)
