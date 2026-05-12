# 先安装：pip install chromadb

import chromadb

# 初始化客户端，在内存中完成操作
chroma_client = chromadb.Client()

# 创建一个合集：类似表，存储向量数据
collection = chroma_client.create_collection(name="mycollection")

# 添加数据，假设这里是需要存储的文本
text1 = "相似性搜索，是指应用程序根据相似性度量从数据库中检索在语义上相似的向量的过程"
text2 = "向量数据库是一种非关系型数据库，专门用于存储和处理向量数据，用于理解数据内在语义"
text3 = "Chroma是一个人工智能原生开源矢量数据库，专注于为RAG提供私有化数据存储和检索。"

# 添加文档，并为每份文档定义一个ID
documents = [text1, text2, text3]
ids = [f"id_{i}" for i in range(1, len(documents)+1)]

# 首次加载时，会下载 all-MiniLM-L6-v2 词嵌入模型来计算向量
collection.add(
    documents=documents,
    # 每条写入的文档可自定义一些元数据，可作为查询条件。与文档一一对应顺序（可选）
    metadatas=[{"keyword": "search"}, {"keyword": "vectordb"},{"keyword": "chroma"}],
    ids=ids
)

# 文档向量的相似度查询
results = collection.query(
    query_texts=["相似性度量"],
    n_results=2
)
print(results)

# 使用get可能通过过滤元数据来查询文档
results = collection.get(
    ids=["id_1", "id_2", "id_3"],   # 可选，指定查询哪些文档
    where={"keyword": "search"},    # 可选，通过元数据进行查询
    where_document={"$contains":"向量"}   # 查询文档中包含“向量”关键字的文档
)
print(results)

