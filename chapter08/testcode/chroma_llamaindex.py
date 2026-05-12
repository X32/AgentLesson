# 先安装：pip install llama-index-vector-stores-chroma

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, Settings
from llama_index.readers.file import MarkdownReader, UnstructuredReader
from llama_index.core.node_parser import MarkdownNodeParser, SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

base_url = "http://192.168.55.200:11434"
Settings.embed_model = OllamaEmbedding(base_url=base_url, model_name="qwen3:8b")
Settings.llm = Ollama(base_url=base_url, model="qwen3:8b", request_timeout=360, thinking=False)


# 添加新文档

# documents = MarkdownReader().load_data(file="./docs/WoniuAI-V6.md")
# chroma_client = chromadb.PersistentClient("./dbstore/chroma")
# chroma_collection = chroma_client.get_or_create_collection("mycollection")
# vectorstore = ChromaVectorStore(chroma_collection=chroma_collection)
# storage_context = StorageContext.from_defaults(vector_store=vectorstore)
# splitter = MarkdownNodeParser()
# index = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context, transformations=[splitter])
# index.set_index_id("WoniuAI-V6")


# 查询文档
# chroma_client = chromadb.PersistentClient("./dbstore/chroma")
# chroma_collection = chroma_client.get_or_create_collection("mycollection")
# vectorstore = ChromaVectorStore(chroma_collection=chroma_collection)
# index = VectorStoreIndex.from_vector_store(vector_store=vectorstore)
#
# retriever = index.as_retriever(similarity_top_k=15)
# print(retriever.retrieve("AI课程分哪几个阶段"))
#
# query_engine = index.as_query_engine(similarity_top_k=15)
# print(query_engine.query("AI课程分哪几个阶段"))





# # 为文档添加元数据，并使用index.insert_nodes来进行持久化保存
# chroma_client = chromadb.PersistentClient("./dbstore/chroma")
# chroma_collection = chroma_client.get_or_create_collection("mycollection")
#
# # 添加文档一
# documents = MarkdownReader().load_data(file="./docs/WoniuAI-QA.txt")
# for document in documents:
#     # 为每一份分段文档定义元数据：filename="WoniuAI-QA.txt"，用于后续过滤
#     document.metadata['filename'] = "WoniuAI-QA.txt"
# vectorstore = ChromaVectorStore(chroma_collection=chroma_collection)
# splitter = MarkdownNodeParser()
# # 如果需要为nodes定义元数据，也可以遍历nodes并为每一个node定义需要的元数据
# nodes_1 = splitter.get_nodes_from_documents(documents)
#
# # 添加文档二
# documents = UnstructuredReader().load_data(file="./docs/Chorma.html")
# for document in documents:
#     document.metadata['filename'] = "Chorma.html"
# vectorstore = ChromaVectorStore(chroma_collection=chroma_collection)
# splitter = SentenceSplitter()
# nodes_2 = splitter.get_nodes_from_documents(documents)
#
# # 也可以通过index.insert_nodes(nodes)而不是StorageContext来持久化保存
# index = VectorStoreIndex.from_vector_store(vector_store=vectorstore)
# index.insert_nodes(nodes_1)
# index.insert_nodes(nodes_2)


# 通过元数据查询到对应的分段文档的编号，并进行删除
chroma_client = chromadb.PersistentClient("./dbstore/chroma")
chroma_collection = chroma_client.get_or_create_collection("mycollection")
vectorstore = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store=vectorstore)

# 删除之前先从WoniuAI-QA.txt提取所有文档（一共只有13份）
retriever = index.as_retriever(similarity_top_k=20)
results = retriever.retrieve("课程")
print(len(results))    # 确认一共有多少个分段文档: 13

# 现在通过元数据从Collection中过滤出WoniuAI-QA.txt相关文档并删除
documents = chroma_collection.get(where={"filename": "WoniuAI-QA.txt"})
document_ids = documents["ids"]    # 输出文档ID的列表

# 删除文档，where过滤条件非必需
chroma_collection.delete(ids=document_ids, where={"filename": "WoniuAI-QA.txt"})

# 删除文档后再次提取所有文档
retriever = index.as_retriever(similarity_top_k=20)
results = retriever.retrieve("课程")    # 结果为2，表明文档已经删除
print(len(results))
