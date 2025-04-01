from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  extra_headers={},
  extra_body={},
  model="deepseek/deepseek-chat-v3-0324:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)