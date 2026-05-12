# 查看文档的分段结果
#
# from llama_index.readers.file import PDFReader, MarkdownReader
#
# # 如果使用MarkdownReader读取MD文件，则分段时会参考MD的章节进行分段
# documents = MarkdownReader().load_data("./docs/WoniuAI-V6.md")
#
# for document in documents:
#     print(document.get_content())
#     print("====================")
#
# # 如果使用PDFReader读取相同内容，则会按照普通分段方案进行分段
# # documents = PDFReader().load_data("./docs/WoniuAI-V6.pdf")
# # for document in documents:
# #     print(document.get_content())
# #     print("====================")






# 利用Ollama进行词嵌入，并创建和保存索引

# import os
# from llama_index.readers.file import MarkdownReader
# from llama_index.core import VectorStoreIndex, Settings
# from llama_index.embeddings.ollama import OllamaEmbedding
#
# from dotenv import load_dotenv
# load_dotenv()
#
# ollama_url = os.getenv('Ollama_Base_Url')
# Settings.embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")
#
# documents = MarkdownReader().load_data("./docs/WoniuAI-V6.md")
# index = VectorStoreIndex.from_documents(documents)
# index.set_index_id("WoniuAI-V6")
# index.storage_context.persist(persist_dir="./dbstore/llamaindex")






# 对已经创建的索引进行读取并进行检索

# import os
# from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage, Settings
# from llama_index.embeddings.ollama import OllamaEmbedding
# from dotenv import load_dotenv
# load_dotenv()
#
# # 检索时也必须指定词嵌入模型，否则无法对问题进行向量化
# ollama_url = os.getenv('Ollama_Base_Url')
# Settings.embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")
#
# # 从指定的目录中加载索引和文档内容
# storage_context = StorageContext.from_defaults(persist_dir='./dbstore/llamaindex')
# # 参数index_id为可选项，不指定则加载整个目录下的索引文件
# index = load_index_from_storage(storage_context, index_id='WoniuAI-V6')
# # index.as_retrieverk只检索结果，无大模型参与回答，默认情况下会检索出2个相似度最高的文档片段
# # retriever = index.as_retriever()
# # 可以通过设置similarity_top_k来调整检索结果的数量
# retriever = index.as_retriever(similarity_top_k=5)
# results = retriever.retrieve("AI课程分哪几个阶段")
# for result in results:
#     print(result.text + "\n\n\n")





# 基于检索结果进行AI问答

# import os
# from llama_index.core import StorageContext, load_index_from_storage, Settings
# from llama_index.embeddings.ollama import OllamaEmbedding
# from llama_index.llms.ollama import Ollama
# from dotenv import load_dotenv
# load_dotenv()
#
# # 检索时也必须指定词嵌入模型，否则无法对问题进行向量化
# ollama_url = os.getenv('Ollama_Base_Url')
# Settings.embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")
# # 要配置让大模型实现对话，必须设置Settings.llm
# Settings.llm = Ollama(base_url=ollama_url, model="qwen3:8b", thinking=False)
#
# storage_context = StorageContext.from_defaults(persist_dir='./dbstore/llamaindex')
# index = load_index_from_storage(storage_context, index_id='WoniuAI-V6')
# # index.as_query_engine集成了检索与对话，将调用大模型对问题进行回复
# query_engine = index.as_query_engine(similarity_top_k=15)
# resp = query_engine.query("AI课程分哪几个阶段")
# print(resp)





# 自定义提示词模板
# import os
# from llama_index.core import StorageContext, load_index_from_storage, Settings, Prompt
# from llama_index.embeddings.ollama import OllamaEmbedding
# from llama_index.llms.ollama import Ollama
# from dotenv import load_dotenv
# load_dotenv()
#
# ollama_url = os.getenv('Ollama_Base_Url')
# Settings.embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")
# Settings.llm = Ollama(base_url=ollama_url, model="qwen3:8b", thinking=False)
#
# storage_context = StorageContext.from_defaults(persist_dir='./dbstore/llamaindex')
# index = load_index_from_storage(storage_context, index_id='WoniuAI-V6')
#
# # context_str和query_str是内置变量，不能修改
# prompt_tmpl = (
#     "以下是为模型提供的上下文信息：\n"
#     "------------------\n"
#     "{context_str}"
#     "\n---------------------\n"
#     "根据这些信息，请回答问题: {query_str}\n"
#     "如果你不知道的话，可以用你已有的知识尽量回复。如果仍然无法回答，"
#     "则请回复用户：对不起，你所提的问题我暂时无法告知答案，建议咨询我们人工客服\n"
# )
# qa_prompt = Prompt(template=prompt_tmpl)
# query_engine = index.as_query_engine(text_qa_template=qa_prompt, similarity_top_k=15)
# resp = query_engine.query("AI课程分哪几个阶段")
# print(resp)




# 流式响应
# import os
# from llama_index.core import StorageContext, load_index_from_storage, Settings
# from llama_index.embeddings.ollama import OllamaEmbedding
# from llama_index.llms.ollama import Ollama
# from dotenv import load_dotenv
# load_dotenv()
#
# # 检索时必须指定与创建索引时相同的词嵌入模型，否则向量化结果无法对比
# ollama_url = os.getenv('Ollama_Base_Url')
# Settings.embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")
# Settings.llm = Ollama(base_url=ollama_url, model="qwen3:8b", thinking=False)
#
# storage_context = StorageContext.from_defaults(persist_dir='./dbstore/llamaindex')
# index = load_index_from_storage(storage_context, index_id='WoniuAI-V6')
# chat = index.as_chat_engine(similarity_top_k=15)
# result = chat.stream_chat("AI课程分哪几个阶段")
# for chunk in result.response_gen:
#     print(chunk, end="")








# 自定义大模型来对检索结果进行流式响应
# import os
# from llama_index.core import StorageContext, load_index_from_storage, Settings
# from llama_index.embeddings.ollama import OllamaEmbedding
# from ollama import Client   # 自定义对话模型，不再需要配置Settings.llm
# from dotenv import load_dotenv
# load_dotenv()
#
# # 检索时必须指定与创建索引时相同的词嵌入模型，否则向量化结果无法对比
# ollama_url = os.getenv('Ollama_Base_Url')
# Settings.embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")
#
# storage_context = StorageContext.from_defaults(persist_dir='./dbstore/llamaindex')
# index = load_index_from_storage(storage_context, index_id='WoniuAI-V6')
# retriever = index.as_retriever(similarity_top_k=15)
#
# query_string = "AI课程分哪几个阶段"
# results = retriever.retrieve(query_string)
# # 遍历results，将检索出来的结果拼接为一个长字符串，作为提示词的一部分
# context_string = ""
# for result in results:
#     context_string += result.text + "\n\n\n"
#
# # 自定义大模型对话来处理RAG，此时原本就是在拼接提示词，所以可以自定义提示词内容
# prompt = f"""请基于以下已知信息，简洁和专业的来回答用户的问题。已知信息内容为：\n
#         ---------------------\n
#         {context_string} \n
#         ---------------------\n
#         请根据这些信息，请回答问题: {query_string} \n
#         如果你不知道如何回答该问题话，请回答不知道 \n """


# # 使用Ollama的qwen3:8b模型进行回答
# client = Client(host=ollama_url)
# messages=[{'role': 'user','content': prompt}]
# stream = client.chat(model='qwen3:8b', messages=messages, stream=True, think=False)
#
# for chunk in stream:
#   print(chunk.message.content, end='', flush=True)


# 使用千问在线模型进行回复
# import dashscope
#
# dashscope.api_key = os.getenv('Dashscope_API_Key')
# messages=[{'role': 'user','content': prompt}]
#
# responses = dashscope.Generation.call(
#         model="qwen-plus",
#         messages=messages,
#         result_format='message',
#         stream=True,
#         incremental_output=True
#     )
# for response in responses:
#     print(response.output.choices[0].message.content, end="")