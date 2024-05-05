import os
from openai import AzureOpenAI
from newspaper import Article
from newspaper import Config
import pandas as pd

# Set your OpenAI API key
AOAI_API_KEY = os.getenv("AOAI_KEY")
AZURE_ENDPOINT = os.getenv("AOAI_ENDPOINT")
API_VERSION = "2024-02-15-preview"

MODEL = "gp4"
TEMPERATURE = 0
TOP_P = 1
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0
MAX_TOKENS = 5
DEBUG = True

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
URL = "https://www.gatesfoundation.org/ideas/articles/artificial-intelligence-ai-development-principles"

# Evaluation prompt template based on G-Eval
EVALUATION_PROMPT_TEMPLATE = """
You will be given one summary written for an article. Your task is to rate the summary on one metric.
Please make sure you read and understand these instructions very carefully. 
Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:

{criteria}

Evaluation Steps:

{steps}

Example:

Source Text:

{document}

Summary:

{summary}

Evaluation Form (scores ONLY):

- {metric_name}
"""

# Metric 1: Relevance

RELEVANCY_SCORE_CRITERIA = """
Relevance(1-5) - selection of important content from the source. \
The summary should include only important information from the source document. \
Annotators were instructed to penalize summaries which contained redundancies and excess information.
"""

RELEVANCY_SCORE_STEPS = """
1. Read the summary and the source document carefully.
2. Compare the summary to the source document and identify the main points of the article.
3. Assess how well the summary covers the main points of the article, and how much irrelevant or redundant information it contains.
4. Assign a relevance score from 1 to 5.
"""

# Metric 2: Coherence

COHERENCE_SCORE_CRITERIA = """
Coherence(1-5) - the collective quality of all sentences. \
We align this dimension with the DUC quality question of structure and coherence \
whereby "the summary should be well-structured and well-organized. \
The summary should not just be a heap of related information, but should build from sentence to a\
coherent body of information about a topic."
"""

COHERENCE_SCORE_STEPS = """
1. Read the article carefully and identify the main topic and key points.
2. Read the summary and compare it to the article. Check if the summary covers the main topic and key points of the article,
and if it presents them in a clear and logical order.
3. Assign a score for coherence on a scale of 1 to 5, where 1 is the lowest and 5 is the highest based on the Evaluation Criteria.
"""

# Metric 3: Consistency

CONSISTENCY_SCORE_CRITERIA = """
Consistency(1-5) - the factual alignment between the summary and the summarized source. \
A factually consistent summary contains only statements that are entailed by the source document. \
Annotators were also asked to penalize summaries that contained hallucinated facts.
"""

CONSISTENCY_SCORE_STEPS = """
1. Read the article carefully and identify the main facts and details it presents.
2. Read the summary and compare it to the article. Check if the summary contains any factual errors that are not supported by the article.
3. Assign a score for consistency based on the Evaluation Criteria.
"""

# Metric 4: Fluency

FLUENCY_SCORE_CRITERIA = """
Fluency(1-3): the quality of the summary in terms of grammar, spelling, punctuation, word choice, and sentence structure.
1: Poor. The summary has many errors that make it hard to understand or sound unnatural.
2: Fair. The summary has some errors that affect the clarity or smoothness of the text, but the main points are still comprehensible.
3: Good. The summary has few or no errors and is easy to read and follow.
"""

FLUENCY_SCORE_STEPS = """
Read the summary and evaluate its fluency based on the given criteria. Assign a fluency score from 1 to 3.
"""

GEMINI_SUMMARY = """
The Bill & Melinda Gates Foundation recognizes the potential of AI to accelerate progress in global health and development, but also acknowledges the risks of inequity and misuse. The foundation is committed to responsible and inclusive development of AI, focusing on access and equity for low-income countries. They have established a task force and advisory committee to guide their approach, adhering to core principles such as co-design, inclusivity, responsible implementation, and transparency. The foundation emphasizes the need to mitigate risks like bias and misinformation, and ensure privacy and security of data. They believe AI can be a powerful tool for positive change, but only if developed and implemented ethically and equitably.
"""

# Function to get article from URL
def get_article(URL, config):
    article = Article(URL, config=config)
    article.download(recursion_counter=2)
    article.parse()
    article.nlp()
    return article.text, article.summary

# Function to save article and summary to disk
def save_article(article_text, reference_summary):
    with open('./data/article.txt', 'w', encoding='utf-8') as f:
        f.write(article_text)
    with open('./data/summary.txt', 'w', encoding='utf-8') as f:
        f.write(reference_summary)

# Function to get evaluation score
def get_geval_score(criteria: str, steps: str, document: str, summary: str, metric_name: str):
    prompt = EVALUATION_PROMPT_TEMPLATE.format(
        criteria=criteria,
        steps=steps,
        metric_name=metric_name,
        document=document,
        summary=summary,
    )
    
    response = client.chat.completions.create(
        model=MODEL,
        messages = [{"role": "user", "content": prompt}],
        temperature = TEMPERATURE, #0
        max_tokens = MAX_TOKENS,   #5
        top_p = TOP_P,             #1
        frequency_penalty = FREQUENCY_PENALTY,  #0
        presence_penalty = PRESENCE_PENALTY,    #0
        stop = None
    )
    return response.choices[0].message.content

evaluation_metrics = {
    "Relevance": (RELEVANCY_SCORE_CRITERIA, RELEVANCY_SCORE_STEPS),
    "Coherence": (COHERENCE_SCORE_CRITERIA, COHERENCE_SCORE_STEPS),
    "Consistency": (CONSISTENCY_SCORE_CRITERIA, CONSISTENCY_SCORE_STEPS),
    "Fluency": (FLUENCY_SCORE_CRITERIA, FLUENCY_SCORE_STEPS),
}

# Main code
client = AzureOpenAI(
      azure_endpoint = AZURE_ENDPOINT,
      api_key=AOAI_API_KEY,
      api_version=API_VERSION
)

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10
article_text, reference_summary = get_article(URL, config)

summaries = {"NLP Summary (1)": reference_summary,
             "Gemini Summary (2)": GEMINI_SUMMARY}

data = {"Evaluation Type": [], "Summary Type": [], "Score": []}

for eval_type, (criteria, steps) in evaluation_metrics.items():
    for summ_type, summary in summaries.items():
        data["Evaluation Type"].append(eval_type)
        data["Summary Type"].append(summ_type)
        result = get_geval_score(criteria, steps, article_text, summary, eval_type)
        score_num = int(float(result.strip()))
        data["Score"].append(score_num)

if DEBUG:
    print(data)

# Assuming data is your dictionary
max_values = {key: max(values) for key, values in data.items()}

# Iterate over the dictionary
for key, values in data.items():
    # Iterate over the values
    for i, value in enumerate(values):
        # If the value is the maximum for that key, append a '*'
        if value == max_values[key]:
            data[key][i] = str(value) + '*'
        else:
            data[key][i] = str(value) + ' '
            
if DEBUG:
    print(data)

# Assuming data is your dictionary
df = pd.DataFrame(data)

# Pivot the DataFrame
pivot_df = df.pivot(index='Evaluation Type', columns='Summary Type', values='Score')

# Print the pivoted DataFrame
print(pivot_df)