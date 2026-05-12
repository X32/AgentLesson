import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

# 持久化保存向量数据到：./dbstore/chroma 目录中
chroma_client = chromadb.PersistentClient("./dbstore/chroma")

url="http://192.168.55.200:11434"
ollama_ef = OllamaEmbeddingFunction(url=url, model_name="qwen3:8b")

# 定义词嵌入模型
class MyEmbeddingFunction(EmbeddingFunction):
    def __init__(self, **kwargs):
        pass      # Chroma要求必须要实现__init__方法

    def __call__(self, texts: Documents) -> Embeddings:
        return ollama_ef.embed_with_retries(texts)

# 新增向量数据，指定词嵌入模型使用Ollama
# collection = chroma_client.create_collection(name="mycollection", embedding_function=MyEmbeddingFunction())
#
# text1 = "相似性搜索，是指应用程序根据相似性度量从数据库中检索在语义上相似的向量的过程"
# text2 = "向量数据库是一种非关系型数据库，专门用于存储和处理向量数据，用于理解数据内在语义"
# text3 = "Chroma是一个人工智能原生开源矢量数据库，专注于为RAG提供私有化数据存储和检索。"
#
# documents=[text1, text2, text3]
# ids=[f"id_{i}" for i in range(1, len(documents)+1)]
#
# collection.add(
#     documents=documents,
#     metadatas=[{"keyword": "search"}, {"keyword": "vectordb"},{"keyword": "chroma"}],
#     ids=ids
# )


# 查询向量数据
# chroma_client = chromadb.PersistentClient("./dbstore/chroma")
# collection = chroma_client.get_collection(name="mycollection", embedding_function=MyEmbeddingFunction())
# results = collection.query(
#     query_texts=["相似性度量"],
#     n_results=2
# )
# print(results)




chroma_client = chromadb.PersistentClient("./dbstore/chroma")
collection = chroma_client.get_collection(name="mycollection", embedding_function=MyEmbeddingFunction())

# 继续新增文档
collection.add(
    documents=["LLamaIndex的任务是通过查询、检索的方式挖掘外部数据的信息，并将其传递给大模型"],
    metadatas=[{"keyword": "llamaindex"}],
    ids=["id_4"]
)

# 对已有文档进行更新
text3_new = "Chroma作为知名的向量数据库，以轻量化、易集成等特性著称，非常适合于中小型项目和研究使用"
collection.update(
    ids=["id_3"],
    documents=[text3_new]   # 将编号为id_3的文档更新为新内容
)

# 删除编号为id_4并且keyword为llamaindex的文档
collection.delete(
    ids=["id_4"],
    where={"keyword": "llamaindex"}
)

# 上述操作均可以通过查询来确认
results = collection.query(
    query_texts=["大模型"],
    n_results=4
)
print(results)