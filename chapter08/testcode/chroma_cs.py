# chroma run --path E:\Workspace\pythonworkspace\AIBook\chapter08\testcode\dbstore\chroma --host 0.0.0.0 --port 8000

import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

chroma_client = chromadb.HttpClient(host='192.168.110.252', port=8000)   # 连接服务器，后续代码不变
url="http://192.168.55.200:11434"
ollama_ef = OllamaEmbeddingFunction(url=url, model_name="qwen3:8b")

class MyEmbeddingFunction(EmbeddingFunction):
    def __init__(self, url):
        self.url=url
    def __call__(self, texts: Documents) -> Embeddings:
        return ollama_ef.embed_with_retries(texts)

collection = chroma_client.get_collection(name="mycollection", embedding_function=MyEmbeddingFunction(url))

results = collection.query(
    query_texts=["相似性度量"],
    n_results=1
)
print(results)