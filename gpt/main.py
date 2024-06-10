import requests
import os
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv("CLOUD_TOKEN")
CATALOG = os.getenv('CATALOG_ID')
AUTH = os.getenv('OAUTH_TOKEN')
TUNED = os.getenv('TUNED')

class GPT:
    def __init__(self, mode='vanila', token=TOKEN, catalog=CATALOG, auth=AUTH, tuned=TUNED):
        self.token = token
        self.catalog = catalog
        self.auth = auth
        self.tuned = tuned
        self.tok = self.get_token()
        self.mode = mode
        if mode == 'vanila':
            self.gpt_url = f'gpt://{self.catalog}/yandexgpt/latest'
        elif mode == 'tuned':
            self.gpt_url = f'ds://{self.tuned}'
        elif mode == 'lite':
            self.gpt_url = f'gpt://{self.catalog}/yandexgpt-lite/latest'
        
    def get_token(self):
        url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        response = requests.post(url, json={'yandexPassportOauthToken': self.auth}).json()
        try:
            result = response['iamToken']
        except Exception as e:
            return None
        else:
            return result

    def gpt_request(self, prompt):
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        if not self.tok:
            return None
        headers = {
            'Authorization': f'Bearer {self.tok}',
            'x-folder-id': self.catalog,
        }

        result = {
          "modelUri": self.gpt_url,
          "completionOptions": {
            "stream": False,
            "temperature": 0.5,
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

        try:
            result = response.json()['result']['alternatives'][0]['message']['text']
            if self.mode == 'tuned':
                result = result[59:].capitalize()
        except Exception as e:
            return "Вышла ошибка..."
        else:
            return result

if __name__ == '__main__':
    #st = 'Работа под авторством Ха-Танха Нгуена и Цзямина Гао "Улучшение логических рассуждений в больших языковых моделях для облегчения юридических приложений" посвящена важнейшему аспекту логических рассуждений в больших языковых моделях (LLM). В то время как LLM демонстрируют впечатляющие возможности понимания языка, их способности к логическим рассуждениям остаются ограниченными. Нгуен и Гао предлагают подход Reinforcement Learning from Logical Feedback (RLLF), разработанный для расширения возможностей логических рассуждений LLM. Работа подчеркивает неразрывную св'
    #print(gpt_request('Если налогоплательщик не получает налоговое уведомление по почте, в каком случае оно считается полученным?'))
    gp = GPT('vanila')
    print(gp.gpt_request('Когда налоговый орган направляет налогоплательщику налоговое уведомление, если обязанность по исчислению суммы налога возлагается на налоговый орган?'))