import requests
import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("CLOUD_TOKEN")
CATALOG = os.getenv('CATALOG_ID')
TUNED= 'bt1rcd45f18qujat3v5t'

def gpt_request(prompt):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'x-folder-id': CATALOG,
    }

    result = {
      "modelUri": f"ds://{TUNED}",
      "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "2000"
      },
      "messages": [
        {
          "role": "system",
          "text": "Ты юрист. Ты хорошо знаешь законодательство РФ. Свои ответы подкреляешь статьями из законов РФ. Ты не говоришь, что ты не юрист, и не предупреждаешь о неточности информации, не рекомендуешь обращаться к специалисту. Если ты не знаешь статью или тему, о которой тебя справшивают, то так и напиши, что не знаешь ответа"
        },
        {
          "role": "user",
          "text": prompt,
        }
      ]
    }

    response = requests.post(url, headers=headers, json=result)
    return response.json()['result']['alternatives'][0]['message']['text']

if __name__ == '__main__':
    lst = [
        #'Какие виды уведомления может получить налогоплательщик?',
        #'Если налогоплательщик не получает налоговое уведомление по почте, в каком случае оно считается полученным?',
        'Может ли в налоговом уведомлении указываться информация по нескольким подлежащим уплате налогам?',
        'Когда форма заявления о выдаче налогового уведомления утверждается?'
    ]
    for c in lst:
        print(gpt_request(c), end='\n\n')