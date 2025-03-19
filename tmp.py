import requests
import utils.database as db

url = 'https://testsites.pythonanywhere.com/gpt'

model = "deepseek/deepseek-chat:free"

data = {
    "data": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Привет!"
                }
            ]
        }
    ],
    "model": model
}

response = requests.post(url, json=data, verify=False)
answer = response.text
print(answer)
