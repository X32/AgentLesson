# 使用SDK获取某个Token的词向量
from ollama import Client

client = Client(host="http://192.168.55.200:11434")
result = client.embed(model="qwen3:8b", input="国")
print(result.embeddings)   # 输出向量值
print(len(result.embeddings[0]))   # 输出向量维度

# 通过HTTP协议获取词向量
import requests

data = {"model":"qwen3:8b", "input":"家"}
resp = requests.post("http://192.168.55.200:11434/api/embed", json=data)
print(resp.json()['embeddings'])