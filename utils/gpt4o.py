import requests
import utils.database as db
from openai import OpenAI

url = 'https://testsites.pythonanywhere.com/gpt'

async def text_generate(user_id, prompt, model):
    print(prompt)
    db.add_message(user_id, f'Я написал: {prompt}')
    history = db.get_message_history(user_id)
    if model == 'gpt-4o':
        model = "google/gemini-2.5-pro-exp-03-25:free"
        tokens = db.get_variable(user_id, 'gpt4o-usage')
        db.set_variable(user_id, 'gpt4o-usage', int(tokens)-1)
    else:
        model = "deepseek/deepseek-chat:free"
        tokens = db.get_variable(user_id, 'gpt4omini-usage')
        db.set_variable(user_id, 'gpt4omini-usage', int(tokens)-1)

    data = {
        "data": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": history
                    }
                ]
            }
        ],
        "model": model
    }

    response = requests.post(url, json=data, verify=False)
    answer = response.text
    print(answer)
    db.add_message(user_id, f'Ты написал: {answer}')
    return answer
