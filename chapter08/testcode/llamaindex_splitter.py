# 理解各种文档分隔器的工作机制




# 固定大小分段：TokenTextSplitter
# from llama_index.core.node_parser import TokenTextSplitter
# from llama_index.readers.file import UnstructuredReader
# from llama_index.core import VectorStoreIndex
#
# 加载文档
# documents = UnstructuredReader().load_data("./docs/WoniuAI-QA.txt")
# # 定义分隔器，并设置每个段落的长度为200，有20个Token可以重叠
# splitter = TokenTextSplitter(chunk_size=200, chunk_overlap=20)
# # 读取分段后的结果，这里是验证分段策略的重点所在
# nodes = splitter.get_nodes_from_documents(documents)
# for node in nodes:
#     print(node.get_content() + "\n=================\n")
#
# # 创建索引时，通过参数 transformations 指定分隔器，该步骤非当前话题必须，后续不再演示
# # transformations 参数可以指定多个分隔器进行混合分隔
# index = VectorStoreIndex.from_documents(documents, transformations=[splitter])




# 固定大小分段：SentenceSplitter
# from llama_index.core.node_parser import SentenceSplitter
# from llama_index.readers.file import UnstructuredReader
#
# documents = UnstructuredReader().load_data("./docs/WoniuAI-QA.txt")
# splitter = SentenceSplitter(chunk_size=500, chunk_overlap=20)
# nodes = splitter.get_nodes_from_documents(documents)
# for node in nodes:
#     print(node.get_content() + "\n=================\n")





# 对未指定分隔器的文档进行分段测试
# from llama_index.readers.file import UnstructuredReader, PDFReader,MarkdownReader
# from llama_index.core import VectorStoreIndex, Settings
# from llama_index.embeddings.ollama import OllamaEmbedding
#
# ollama_url = "http://192.168.55.200:11434"
# Settings.embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")
# documents = UnstructuredReader().load_data("./docs/WoniuAI-V6.txt")
# print(len(documents))  # 查看预分段数量情况
# index = VectorStoreIndex.from_documents(documents)
# retriever = index.as_retriever(similarity_top_k=50)
# results = retriever.retrieve("AI课程分哪几个阶段")
# for result in results:
#     print(result.text + "\n\n\n")    # 查看检索出的分段数据




# 语义分段：
# from llama_index.core.node_parser import SemanticSplitterNodeParser
# from llama_index.readers.file import UnstructuredReader
# from llama_index.embeddings.ollama import OllamaEmbedding
#
# ollama_url = "http://192.168.55.200:11434"
# embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")
# documents = UnstructuredReader().load_data("./docs/WoniuAI-V6.txt")
#
# splitter = SemanticSplitterNodeParser.from_defaults(buffer_size=1, breakpoint_percentile_threshold=60, embed_model=embed_model)
#
# nodes = splitter.get_nodes_from_documents(documents)
# print(len(nodes))   # 111
# for node in nodes:
#     print(node.get_content() + "\n=================\n")






# 递归分段
# from llama_index.core.node_parser import HierarchicalNodeParser
# from llama_index.readers.file import UnstructuredReader
#
# documents = UnstructuredReader().load_data("./docs/WoniuAI-QA.txt")
#
# # 将文档分别按照1024、512、256进行分段，会得到更多大小不一的段落，内容有所重复
# # 相当于使用了三种不同Chunk_Size大小的SentenceSplitter来进行分段
# splitter = HierarchicalNodeParser.from_defaults(chunk_sizes=[1024, 512, 256])
# nodes = splitter.get_nodes_from_documents(documents)
# print(len(nodes))
# for node in nodes:
#     print(node.get_content() + "\n=================\n")






# 文档结构分段：
# from llama_index.core.node_parser import MarkdownNodeParser, HTMLNodeParser, JSONNodeParser
# from llama_index.readers.file import FlatReader
# from pathlib import Path
#
# # JSON分隔器，FlatReader对象加载文档时必须由Path对象指定路径
# documents = FlatReader().load_data(Path("./docs/Exam.json"))
# splitter = JSONNodeParser()
# nodes = splitter.get_nodes_from_documents(documents)
# print(len(nodes))
#
# # HTML分隔器
# documents = FlatReader().load_data(Path("./docs/Chorma.html"))
# splitter = HTMLNodeParser()
# nodes = splitter.get_nodes_from_documents(documents)
# print(len(nodes))
#
# # Markdown分隔器
# documents = FlatReader().load_data(Path("./docs/WoniuAI-V6.md"))
# splitter = MarkdownNodeParser()
# nodes = splitter.get_nodes_from_documents(documents)
# print(len(nodes))






# 自定义多分隔器策略
from llama_index.core.node_parser import SentenceSplitter, MarkdownNodeParser
from llama_index.readers.file import UnstructuredReader
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding

ollama_url = "http://192.168.55.200:11434"
Settings.embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")

documents = UnstructuredReader().load_data("./docs/WoniuAI-V6.txt")
splitter_1 = MarkdownNodeParser()
splitter_2 = SentenceSplitter(chunk_size=512)
index = VectorStoreIndex.from_documents(documents, transformations=[splitter_1, splitter_2])
retriever = index.as_retriever(similarity_top_k=50)
results = retriever.retrieve("AI课程分哪几个阶段")
print(len(results))
for result in results:
    print(result.text + "\n\n\n")



