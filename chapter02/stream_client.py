import requests, json

url = "http://127.0.0.1:8000/stream"
data = {"content":"你好，你是谁？"}
resp = requests.post(url=url, json=data, stream=True)
for chunk in resp.iter_lines():
    print(json.loads(chunk.decode())['content'], end='')