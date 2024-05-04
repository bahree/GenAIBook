# # conda install -c conda-forge newspaper3k evaluate
# # conda install -c conda-forge evaluate
# # conda install -c huggingface -c conda-forge datasets
# # pip install bert_score 

# import os
# from openai import AzureOpenAI
# from newspaper import Article
# from newspaper import Config
# import evaluate

# # Set your OpenAI API key
# AOAI_API_KEY = os.getenv("AOAI_KEY")
# AZURE_ENDPOINT = os.getenv("AOAI_ENDPOINT")
# API_VERSION = "2024-02-15-preview"

# MODEL = "gp4"
# TEMPERATURE = 0.75
# TOP_P = 0.95
# FREQUENCY_PENALTY = 0
# PRESENCE_PENALTY = 0
# MAX_TOKENS = 250
# DEBUG = False
# SAVE_DATA = True

# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

# config = Config()
# config.browser_user_agent = USER_AGENT
# config.request_timeout = 10

# print("Downloading article...")
# # Fetch and parse news article
# URL = "https://www.gatesfoundation.org/ideas/articles/artificial-intelligence-ai-development-principles"
# article = Article(URL, config=config)
# article.download()
# article.parse()
# article.nlp()

# # Extract article text and reference summary
# article_text = article.text
# reference_summary = article.summary

# if DEBUG:
#   if SAVE_DATA:
#     with open('./data/article.txt', 'w', encoding='utf-8') as f:
#         f.write(article_text)
#     with open('./data/summary.txt', 'w', encoding='utf-8') as f:
#         f.write(reference_summary)
      
#     print("Article Text:")
#     print(article_text)
#     print("\nReference Summary:")
#     print(reference_summary)
#     input("Press Enter to continue...")

# # Generate summary using OpenAI API
# prompt = f"Summarize the following article:\n\n{article_text}"
# conversation = [{"role": "system", "content": "You are a helpful assistant."}]
# conversation.append({"role": "user", "content": prompt})

# # Initialize OpenAI client
# client = AzureOpenAI(
#   azure_endpoint = AZURE_ENDPOINT, 
#   api_key=AOAI_API_KEY,  
#   api_version=API_VERSION
# )

# response = client.chat.completions.create(
#     model=MODEL,
#     messages = conversation,
#     temperature = TEMPERATURE,
#     max_tokens = MAX_TOKENS,
#     top_p = TOP_P,
#     frequency_penalty = FREQUENCY_PENALTY,
#     presence_penalty = PRESENCE_PENALTY,
#     stop = None
# )

# generated_summary = message_response = response.choices[0].message.content.strip()

# # Calculate BLEU score
# metric = evaluate.load("bleu", trust_remote_code=True)
# bleu_score = metric.compute(predictions=[generated_summary], references=[reference_summary])

# # Calculae the ROUGE score
# metric = evaluate.load("rouge", trust_remote_code=True)
# rouge_score = metric.compute(predictions=[generated_summary], references=[reference_summary])

# # Print scores and summaries
# print(f"BLEU score: {bleu_score}")
# print(f"ROUGE score: {rouge_score}")
# # print("-" * 50)
# # print(f"\nReference Summary:\n{reference_summary}")
# # print(f"\nGenerated Summary:\n{generated_summary}")

import os
from openai import AzureOpenAI
from newspaper import Article
from newspaper import Config
import evaluate
from bert_score import BERTScorer

# Set your OpenAI API key
AOAI_API_KEY = os.getenv("AOAI_KEY")
AZURE_ENDPOINT = os.getenv("AOAI_ENDPOINT")
API_VERSION = "2024-02-15-preview"

MODEL = "gp4"
TEMPERATURE = 0.75
TOP_P = 0.95
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0
MAX_TOKENS = 250
DEBUG = True
SAVE_DATA = True

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
URL = "https://www.gatesfoundation.org/ideas/articles/artificial-intelligence-ai-development-principles"

def get_article(URL, config):
    article = Article(URL, config=config)
    article.download(recursion_counter=2)
    article.parse()
    article.nlp()
    return article.text, article.summary

def save_article(article_text, reference_summary):
    directory = './data'
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f'{directory}/gates_foundation_article.txt', 'w', encoding='utf-8') as f:
        f.write(article_text)

    with open(f'{directory}/summary.txt', 'w', encoding='utf-8') as f:
        f.write(reference_summary)
        
def generate_summary(client, article_text):
    prompt = f"Summarize the following article:\n\n{article_text}"
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]
    conversation.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=MODEL,
        messages = conversation,
        temperature = TEMPERATURE,
        max_tokens = MAX_TOKENS,
        top_p = TOP_P,
        frequency_penalty = FREQUENCY_PENALTY,
        presence_penalty = PRESENCE_PENALTY,
        stop = None
    )
    return response.choices[0].message.content.strip()
  
def calculate_scores(generated_summary, reference_summary):
  try:
    if DEBUG:
        print("Generated Summary:")
        print(generated_summary)
        print("\nReference Summary:")
        print(reference_summary)
          
    metric = evaluate.load("bleu", trust_remote_code=True)
    bleu_score = metric.compute(predictions=[generated_summary], references=[reference_summary])

    metric = evaluate.load("rouge", trust_remote_code=True)
    rouge_score = metric.compute(predictions=[generated_summary], references=[reference_summary])
    
    scorer = BERTScorer(lang="en")
    p1, r1, f1 = scorer.score([generated_summary], [reference_summary])
    bert_score = f"Precision: {p1} Recall: {r1} F1 Score: {f1.tolist()[0]}"
    
    if DEBUG:
        print(f"BLEU score: {bleu_score}")
        print(f"ROUGE score: {rouge_score}")
        print(f"BERT score: {bert_score}")
    
    return bleu_score, rouge_score, bert_score
  except Exception as e:
    print(f"Error calculating scores: {e}")
    return 0, 0  # return a default value

# Main code
client = AzureOpenAI(
      azure_endpoint = AZURE_ENDPOINT,
      api_key=AOAI_API_KEY,
      api_version=API_VERSION
)

print("Downloading article...")
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10
article_text, reference_summary = get_article(URL, config)

if DEBUG and SAVE_DATA:
  save_article(article_text, reference_summary)

generated_summary = generate_summary(client, article_text)
bleu_score, rouge_score, bert_score = calculate_scores(generated_summary, reference_summary)

print(f"BLEU score: {bleu_score}")
print(f"ROUGE score: {rouge_score}")
print(f"BERT score: {bert_score}")
