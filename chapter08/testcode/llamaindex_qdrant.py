# 最新下载：1.14.1版本 https://github.com/qdrant/qdrant
# 还需要安装：pip install llama-index-vector-stores-qdrant

from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext, Settings
from llama_index.readers.file import UnstructuredReader
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from llama_index.core.node_parser import SentenceSplitter


base_url = "http://192.168.55.200:11434"
documents = UnstructuredReader().load_data("./docs/Go-Huawei.txt")

Settings.embed_model = OllamaEmbedding(base_url=base_url, model_name="qwen3:8b")
Settings.llm = Ollama(base_url=base_url, model="qwen3:8b", thinking=False)

# 读取qwen3:8b模型的向量维度,因为
n_dim = len(Settings.embed_model.get_query_embedding("中"))

qdrant_client = QdrantClient(host="127.0.0.1", port=6333)

# 新增并查询
if not qdrant_client.collection_exists("huawei"):
    qdrant_client.create_collection(
         collection_name="huawei",
         vectors_config=VectorParams(
            size=n_dim,
            distance=Distance.COSINE,
        ),
    )

# 分段创建索引
vectorstore = QdrantVectorStore(collection_name="huawei", client=qdrant_client)
storage_context = StorageContext.from_defaults(vector_store=vectorstore)
splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
index = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context, transformations=[splitter])

# 查询并回复
query_engine = index.as_query_engine(similarity_top_k=20)
response = query_engine.query("请总结华为的管理风格")
print(response)



# 新增成功后，直接总结
# vectorstore = QdrantVectorStore(collection_name="huawei", client=qdrant_client)
# index = VectorStoreIndex.from_vector_store(vector_store=vectorstore)
# query_engine = index.as_query_engine(similarity_top_k=20)
# response = query_engine.query("请总结华为的管理风格")
# print(response)