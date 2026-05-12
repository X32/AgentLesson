from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OpenRouter_API_Key")
)

completion = client.chat.completions.create(
  model="anthropic/claude-3.7-sonnet",
  messages=[
    {"role": "user","content": "你好，你是谁？"}
  ],
  stream=True)

for chunk in completion:
    print(chunk.choices[0].delta.content, end="")
