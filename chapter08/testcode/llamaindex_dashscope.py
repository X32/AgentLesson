# 需要先安装
# pip install llama-index-llms-dashscope
# pip install llama-index-indices-managed-dashscope





# 加载文档、创建索引（百炼云端存储）

# import os
# from llama_index.readers.dashscope.base import DashScopeParse
# from llama_index.readers.dashscope.utils import ResultType
# from llama_index.indices.managed.dashscope import DashScopeCloudIndex
#
# from dotenv import load_dotenv
# load_dotenv()
#
# # 读取百炼平台的业务空间ID
# workspace_id = os.getenv('DashScope_Workspace_Id')
#
# # 指定要加载的文件，并创建知识库（索引）
# file = ["./docs/WoniuAI-V6.md", "./docs/Go-Huawei.txt"]
# parse = DashScopeParse(result_type=ResultType.DASHSCOPE_DOCMIND)
# documents = parse.load_data(file_path=file)
# index = DashScopeCloudIndex.from_documents(documents=documents, name="Woniu-Index-1", workspace_id=workspace_id)
# print(index)


# 第二种方式：使用文档解析器解析一个文件夹内指定类型的文件
# from llama_index.core import SimpleDirectoryReader
#
# parse = DashScopeParse(result_type=ResultType.DASHSCOPE_DOCMIND)
# # 定义不同文档类型的解析器
# file_extractor = {".md": parse, '.txt': parse, '.docx': parse}
# # 读取文件夹，提取和解析文件信息
# documents = SimpleDirectoryReader(
#     "./docs", file_extractor=file_extractor
# ).load_data(num_workers=1)



# 检索文档分段，或基于检索结果进行回复

import os
from llama_index.core import Settings
from llama_index.llms.dashscope import DashScope
from llama_index.indices.managed.dashscope import DashScopeCloudIndex
from dotenv import load_dotenv
load_dotenv()
workspace_id = os.getenv('DashScope_Workspace_Id')

# 仅检索文档段落
index = DashScopeCloudIndex(name="Woniu-Index-1")
retriever = index.as_retriever(rerank_top_n=10, workspace_id=workspace_id)
nodes = retriever.retrieve("华为股权改革")
for node in nodes:
    print(node)    # 可查看相似度评分

# 调用大模型进行对话（此处使用qwen-max以与词嵌入模型进行区分）
Settings.llm = DashScope(model_name="qwen-max", api_key=os.getenv('Dashscope_API_Key'))
index = DashScopeCloudIndex(name="Woniu-Index-1")
query_engine = index.as_query_engine(rerank_top_n=5, workspace_id=workspace_id)
result = query_engine.query("AI课程分哪几个阶段")
print(result)

