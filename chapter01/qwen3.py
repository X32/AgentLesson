# 通过OpenAI对接
import os

# from openai import OpenAI
# import json, os
#
# from dotenv import load_dotenv
# load_dotenv()
#
# client = OpenAI(
#     api_key=os.getenv("Dashscope_API_Key"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
# )
#
# completion = client.chat.completions.create(
#     # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
#     model="qwen-plus",
#     messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
#                 {'role': 'user', 'content': '你是谁？'}],
#     stream=True,
#     stream_options={"include_usage": True}
#     )
#
# # 在流式响应中查看JSON的数据结构，便于提取其中的响应正文
# # for chunk in completion:
# #     print(chunk.model_dump_json())
#
# # 输出响应正文（根据JSON数据结构按层次输出即可）
# for chunk in completion:
#     if len(chunk.choices) > 0:
#         print(chunk.choices[0].delta.content, end="")




# 通过Dashscope进行对接

# import os, dashscope
#
# from dotenv import load_dotenv
# load_dotenv()
#
# messages = [
#         {'role':'system','content':'you are a helpful assistant'},
#         {'role': 'user','content': '你是谁？'}
#     ]
# responses = dashscope.Generation.call(
#         api_key=os.getenv('Dashscope_API_Key'),
#         model="qwen-plus",
#         messages=messages,
#         result_format='message',
#         stream=True,
#         incremental_output=True
#     )
# for response in responses:
#     print(response.output.choices[0].message.content, end="")




# 通过HTTP协议进行调用

import requests, json

from dotenv import load_dotenv
load_dotenv()

url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
data = {
    "model": "qwen-plus",
    "messages":[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"}
    ],
    "stream": True
}
header = {"Authorization": f"Bearer {os.getenv('Dashscope_API_Key')}"}
response = requests.post(url=url, headers=header, json=data, stream=True)

# 输出格式类似于以下内容，所以需要特殊处理
# b'data: {"choices":[{"delta":{"content":"","role":"assistant"},........."}'
# b''
# b'data: {"choices":[{"finish_reason":null,"delta":{"content":"\xe6\x88\x91\xe6\x98\xaf"},.....}'
for chunk in response.iter_lines():
    chunk_list = chunk.decode('utf-8').split("data: ")
    for line in chunk_list:
        if len(line) > 10:
            chunk_json = json.loads(line)
            print(chunk_json['choices'][0]['delta']['content'], end='')