from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# # 使用HTTP协议进行连接
# client = QdrantClient(host="192.168.110.252", port=6333)
# # 也可以使用GRPC协议进行连接
# # client = QdrantClient(host="192.168.110.252", grpc_port=6334, prefer_grpc=True)
#
# # 定义词嵌入模型,使用Chroma已经下载过的模型
# encoder = SentenceTransformer("all-MiniLM-L6-v2")
#
# # 创建Collection,并指定向量维度和相似度查询方法
# if not client.collection_exists("my_collection"):
#     client.create_collection(
#         collection_name="my_collection",
#         vectors_config=VectorParams(
#             size=encoder.get_sentence_embedding_dimension(),
#             distance=Distance.COSINE,
#         ),
#     )
#
# # 定义需要创建索引的文档内容
# text1 = "相似性搜索，是指应用程序根据相似性度量从数据库中检索在语义上相似的向量的过程"
# text2 = "向量数据库是一种非关系型数据库，专门用于存储和处理向量数据，用于理解数据内在语义"
# text3 = "Chroma是一个人工智能原生开源矢量数据库，专注于为RAG提供私有化数据存储和检索。"
# text4 = "LLamaIndex的任务是通过查询、检索的方式挖掘外部数据的信息，并将其传递给大模型"
# documents = [text1, text2, text3, text4]
#
# # 定义一个Points列表,每个Points相当于一个分段文档
# points = []
# for idx, text in enumerate(documents):
#     # 此处必须要指定payload参数,里面可以保存元数据,更需要保存原始文本
#     point = PointStruct(id=idx, vector=encoder.encode(text).tolist(), payload={"text": text})
#     points.append(point)
#
# # 上传文档并完成索引的创建
# client.upload_points(collection_name="my_collection", points=points)
#
# client.close()


# 纯查询
client = QdrantClient(host="192.168.110.252", port=6333)
encoder = SentenceTransformer("all-MiniLM-L6-v2")

# 进行查询,并按照余弦相似度从高到低排序
results = client.query_points(
    collection_name="my_collection",
    query=encoder.encode("相似性度量").tolist(),
    limit=2,
).points

print(results)

# 可以直接读取到score和payload
for result in results:
    print(result.score, result.payload['text'])

client.close()