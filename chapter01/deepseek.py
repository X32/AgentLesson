# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# load_dotenv()
#
# client = OpenAI(api_key=os.getenv("DeepSeek_API_Key"), base_url="https://api.deepseek.com")
#
# completion = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "你好，你是谁？"},
#     ],
#     stream=True
# )
#
# for chunk in completion:
#     print(chunk.choices[0].delta.content, end="")




import os, requests, json
from dotenv import load_dotenv
load_dotenv()

url = "https://api.deepseek.com/chat/completions"
data = {
        "model": "deepseek-chat",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "你好，你是谁？"}
        ],
        "stream": True
      }
header = {"Authorization": f"Bearer {os.getenv('DeepSeek_API_Key')}"}
response = requests.post(url=url, headers=header, json=data, stream=True)
for chunk in response.iter_lines():
    chunk_list = chunk.decode('utf-8').split("data: ")
    for line in chunk_list:
        if len(line) > 10:
            chunk_json = json.loads(line)
            print(chunk_json['choices'][0]['delta']['content'], end='')