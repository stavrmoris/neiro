import requests
import utils.database as db

url = 'https://bot.aioneplace.com/gpt'

async def image_generate(user_id, prompt):
    tokens = int(db.get_variable(user_id, 'dalle-usage'))
    db.set_variable(user_id, 'dalle-usage', tokens-1)
    data = {"prompt": prompt}
    response = requests.post(url, json=data, verify=False)

    return response.text
