import requests
import utils.database as db
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

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

    completion = client.chat.completions.create(
        extra_headers={},
        extra_body={},
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{history}"
                    }
                ]
            }
        ]
    )
    answer = completion.choices[0].message.content
    print(answer)
    db.add_message(user_id, f'Ты написал: {answer}')
    return answer
