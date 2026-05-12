# 使用SentenceTransformerRerank对检索结果重新排序
# from llama_index.core.indices.postprocessor import SentenceTransformerRerank
# reranker = SentenceTransformerRerank(model="BAAI/bge-reranker-v2-m3")

import os
from llama_index.core import StorageContext, load_index_from_storage, Settings, QueryBundle
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.indices.postprocessor import SentenceTransformerRerank
from dotenv import load_dotenv
load_dotenv()
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# 常规设置
ollama_url = os.getenv('Ollama_Base_Url')
# ollama_url = "http://localhost:11434"   # 显存不够，Ollama会停止，导致无法完成对话
Settings.embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")
Settings.llm = Ollama(base_url=ollama_url, model="qwen3:8b", thinking=False)

# 加载重排序模型，只挑选最相似的5条结果交由大模型处理
reranker = SentenceTransformerRerank(model="BAAI/bge-reranker-v2-m3", top_n=5, device="cuda:0")

storage_context = StorageContext.from_defaults(persist_dir='./dbstore/llamaindex')
index = load_index_from_storage(storage_context, index_id='WoniuAI-V6')

# 定义查询引擎时，需要指定reranker, 参数similarity_top_k=15表示首次检索15条数据
query_engine = index.as_query_engine(similarity_top_k=15, node_postprocessors=[reranker])

# 通过构建查询引擎本身的检索数据，来确定重排序是否生效
retrievers = query_engine.retrieve(QueryBundle("AI课程分哪几个阶段"))
print(len(retrievers))   # 如果记录为5条，则说明重排序生效
for retriever in retrievers:
    print(retriever.text + "\n==================\n")

# 正常进行响应, 根据响应结果可知，回答正确。
result = query_engine.query("AI课程分哪几个阶段")
print(result)