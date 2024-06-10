import requests
import numpy as np
from scipy.spatial.distance import cdist
import os
from dotenv import load_dotenv

load_dotenv()

FOLDER_ID = os.getenv('CATALOG_ID')
IAM_TOKEN = os.getenv("CLOUD_TOKEN")
print(FOLDER_ID, IAM_TOKEN)

doc_uri = f"emb://{FOLDER_ID}/text-search-doc/latest"
query_uri = f"emb://{FOLDER_ID}/text-search-query/latest"

embed_url = "https://llm.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {IAM_TOKEN}", "x-folder-id": f"{FOLDER_ID}"}

doc_texts = [
    "Работа под авторством Ха-Танха Нгуена и Цзямина Гао 'Улучшение логических рассуждений в больших языковых моделях для облегчения юридических приложений' посвящена важнейшему аспекту логических рассуждений в больших языковых моделях (LLM). В то время как LLM демонстрируют впечатляющие возможности понимания языка, их способности к логическим рассуждениям остаются ограниченными. Нгуен и Гао предлагают подход Reinforcement Learning from Logical Feedback (RLLF), разработанный для расширения возможностей логических рассуждений LLM. Работа подчеркивает неразрывную св"
]

query_text = "когда день рождения Пушкина?"

def get_embedding(text: str, text_type: str = "doc") -> np.array:
    query_data = {
        "modelUri": doc_uri if text_type == "doc" else query_uri,
        "text": text,
    }

    return np.array(
        requests.post(embed_url, json=query_data, headers=headers).json()
    )

print(get_embedding(doc_texts[0]), 'sch')

'''
query_embedding = get_embedding(query_text, text_type="query")
docs_embedding = [get_embedding(doc_text) for doc_text in doc_texts]

# Вычисляем косинусное расстояние
dist = cdist(query_embedding[None, :], docs_embedding, metric="cosine")

# Вычисляем косинусное сходство
sim = 1 - dist

# most similar doc text
print(doc_texts[np.argmax(sim)])
'''
