# 先安装：pip install llama-index
# pip install llama-index-llms-ollama
# pip install llama-index-embeddings-ollama
# pip install unstructured

# llamaindex默认自己有一个文本向量数据库，但是适用于小数据量，量大则需要整合Chroma或QDrant等专业数据库

# Ollama作为词嵌入和对话模型
import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.readers.file import UnstructuredReader, PDFReader, MarkdownReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from dotenv import load_dotenv
load_dotenv()

ollama_url = os.getenv('Ollama_Base_Url')   # http://192.168.55.200:11434

# 通过Settings来配置词嵌入模型，此处使用Ollama的qwen3:8b进行词嵌入
Settings.embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")
# 配置大模型对话模型，此处也使用Ollama，如有需要，可以加载其他模型
# request_timeout=360：请求超时时间， thinking=False：不进行思考，节省响应时间
Settings.llm = Ollama(base_url=ollama_url, model="qwen3:8b", request_timeout=360, thinking=False)

# 从docs目录中加载所有文档，如果文档较多，词嵌入和索引过程耗时较长
# documents = SimpleDirectoryReader(input_dir="./docs").load_data()
# 也可以指定打开某个特定文档，以加快处理过程，让实验快速启动
documents = MarkdownReader().load_data("./docs/WoniuAI-V6.md")

# 对文档进行索引
index = VectorStoreIndex.from_documents(documents)

# 将向量持久化保存到dbstore目录中，并且设置索引ID为：WoniuAI-V6
# 后续可以通过索引编号来对索引进行过滤，以指定更小范围的内容进行检索
index.set_index_id("WoniuAI-V6")

# 将索引持久化保存到 ./dbstore/llamaindex 目录中
index.storage_context.persist(persist_dir="./dbstore/llamaindex")

# 通过提示词检索相关文档分段，并通过大模型进行回复
query_engine = index.as_query_engine()
resp = query_engine.query("AI课程分哪几个阶段")
print(resp)

# 输出结果
# AI课程分为三个主要阶段，每个阶段包含多个项目实战，帮助学员逐步掌握AI技术并实现实际应用。
# 第一阶段包含网店销售额预测、加州房价预测、鸢尾花分类、心脏病患分类、手写数字识别、图片验证码识别、
# 人脸识别与考勤、活体检测、OCR图片文字识别、银行客户流失预测、狗狗品种识别、CIFAR物品识别等项目。
# 第二阶段涵盖文本摘要、词向量模型训练、百度百科文章分类模型、N-Gram与NPLM文本生成、RNN生成外卖评论、
# RNN生成唐诗、Seq2Seq实现机器翻译、Transformer与GPT模型训练、基于Bert的二次训练实现今日头条新闻分类模型、
# 模型微调与量化、StableDiffusion文生图等项目。第三阶段则包括网页语音版问答系统、每日新闻摘要、
# 在线智能客服、AI智慧课堂、智能随身导游、会议智能秘书、语音识别记分牌、向量数据库、用户画像与产品推荐等AI应用项目。
# 此外，物联网专业的智能驾驶项目也对学员开放。









# from llama_index.core import StorageContext, load_index_from_storage
#
# storage_context = StorageContext.from_defaults(persist_dir='./dbstore/llamaindex')
# index = load_index_from_storage(storage_context, index_id='WoniuAI-V6')
# query_engine = index.as_query_engine(similarity_top_k=2)
# resp = query_engine.query("AI课程分哪几个阶段")
# print(resp)


# 添加提示词模板
# storage_context = StorageContext.from_defaults(persist_dir='./dbstore/llamaindex')
# index = load_index_from_storage(storage_context, index_id='WoniuAI-V5.md')
#
# # context_str和query_str是内置变量，不能修改
# prompt_tmpl = (
#     "以下是为模型提供的上下文信息：\n"
#     "------------------\n"
#     "{context_str}"
#     "\n---------------------\n"
#     "根据这些信息，请回答问题: {query_str}\n"
#     "如果您不知道的话，请回答不知道\n"
# )
# qa_prompt = Prompt(template=prompt_tmpl)
# query_engine = index.as_query_engine(text_qa_template=qa_prompt)
# # response = query_engine.query("AI课程分为几个阶段")
# response = query_engine.query("广告投放效果评估项目情况")
# print(response)
#
# # 读取原始文档内容，可以自主定义大模型来进行总结
# retriever = index.as_retriever()
# print(retriever.get_prompts())
# print(retriever.retrieve())






# 分段存储和检索：默认使用SentenceSplitter,2048个节点，也可以多分隔器混合
# splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
# documents = MarkdownReader(remove_hyperlinks=False).load_data("./docs/WoniuAI-V5.md")
# index = VectorStoreIndex.from_documents(documents, transformations=[splitter])
# index.set_index_id("WoniuAI-V5.md")
# index.storage_context.persist(persist_dir="./dbstore/llamaindex")