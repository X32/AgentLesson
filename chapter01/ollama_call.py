from ollama import Client

client = Client(host="http://localhost:11434")
messages=[{
    'role': 'user',
    'content': '你好，你是谁？',
  }]
response = client.chat(model='qwen3:8b', messages=messages, think=False)
# print(response['message']['content'])
print(response.message.content)


# from ollama import Client
#
# client = Client(host="http://localhost:11434")
# messages=[{
#     'role': 'user',
#     'content': '你好，你是谁？',
#   }]
# stream = client.chat(model='qwen3:8b', messages=messages, stream=True)
#
# for chunk in stream:
#   print(chunk.message.content, end='', flush=True)



# import requests, json
#
# url = "http://localhost:11434/api/generate"
# data = {"model":"qwen3:8b",
#         "prompt":"你好，你是谁？",
#         "stream":True}
# resp = requests.post(url=url, json=data, stream=True)
# for line in resp.iter_lines():
#     data = json.loads(line)
#     print(data['response'], end='')
#     if data['done'] == True:
#         print(f"\n总Token为：{data['eval_count']}")



# 多轮对话
# import requests, json
#
# url = "http://localhost:11434/api/chat"
# # 定义消息列表用于保存历史消息, 其中 role=system代表是系统提示词
# messages = [{"role": "system", "content": "你是一名优秀的智能助手，请直接给出答案，不需要展示思考过程。"}]
#
# def send_message(message):
#     # 先将用户提问保存到历史消息中
#     messages.append({"role": "user", "content": message})
#
#     data = {
#         "model": "qwen3:8b",
#         "messages": messages,
#         "stream":True
#     }
#     resp = requests.post(url=url, json=data, stream=True)
#     reply = ""   # 由于是流式响应，所以需要将响应内容添加到reply字符串中用于保存历史
#     for line in resp.iter_lines():
#         data = json.loads(line)
#         tokens = data["message"]["content"]
#
#         # 过滤掉<think>标签并将空白字符清除
#         if "think" not in tokens and len(tokens.strip()) >= 1:
#             print(tokens, end='')
#             reply += tokens
#
#     # 将AI的回答也保存到历史消息中
#     messages.append({"role": "assistant", "content": reply})
#
# if __name__ == '__main__':
#     while True:
#         question = input("\n请输入你的问题：")
#         send_message(question)