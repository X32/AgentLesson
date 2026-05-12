from llama_index.core import VectorStoreIndex, Settings, StorageContext, Prompt, load_index_from_storage
from llama_index.core.node_parser.interface import NodeParser
from llama_index.core.schema import BaseNode, TextNode
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from typing import List
from pydantic import Field
from llama_index.readers.file import DocxReader, UnstructuredReader
import os, json, dashscope
from ollama import Client
from dotenv import load_dotenv
load_dotenv()

ollama_url = os.getenv('Ollama_Base_Url')
Settings.embed_model = OllamaEmbedding(base_url=ollama_url, model_name="qwen3:8b")
Settings.llm = Ollama(base_url=ollama_url, model="qwen3:8b", request_timeout=360, thinking=False)

class CustomSplitter(NodeParser):

    # 由于pydantic会检验参数，所以必须在此处先定义
    prompt : str = Field(default=None, description="大模型分块提示词")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 从初始化参数中读取prompt
        self.prompt = kwargs.get("prompt")

    # 参数和返回值定义必须按照规范来
    def _parse_nodes(self, nodes: List[BaseNode], **kwargs) -> List[BaseNode]:
        all_nodes: List[BaseNode] = []
        for node in nodes:
            content = node.get_content()
            sections = self.__chat_llm(self.prompt, content)
            sections_json = eval(sections)
            for section in sections_json:
                keyword = section["keyword"]
                content = section["content"]
                node = TextNode(text=f"{keyword}: {content}")
                all_nodes.append(node)

        return all_nodes

    # 利用大模型进行分段，并返回一个JSON，格式为：{"keyword": keyword, "content": content}
    def __chat_llm(self, prompt, content):
        # 使用本地Ollama进行分段
        # client = Client(host=ollama_url)
        # messages = [{'role': 'system', 'content': '你擅长分析和处理任意文档内容，并通过分析文档结构和语义来对文档进行分段处理。'},
        #             {'role': 'user', 'content': prompt + content}]
        # completion = client.chat(model='qwen3:8b', messages=messages, think=False)
        # return completion.message.content.replace("```json", "").replace("```", "")

        # 使用云端大模型进行分段
        messages = [{'role': 'system', 'content': '你擅长分析和处理任意文档内容，并通过分析文档结构和语义来对文档进行分段处理。'},
                    {'role': 'user', 'content': prompt + content}]

        responses = dashscope.Generation.call(
            api_key=os.getenv('Dashscope_API_Key'),
            model="qwen-plus",
            messages=messages,
        )
        return responses.output.text.replace("```json", "").replace("```", "")


if __name__ == '__main__':
    prompt = '''
    #目的# \n
    请针对以下提供的文本内容进行分段处理，用于RAG知识库检索生成，提供给用户最为准确的分块内容。\n
    #要求# \n
    1、不能对原文内容进行总结，必须原文输出，且按照以下要求进行分段。
    2、如果文档是MarkDown或Word格式，如果存在章节，则优先按照章节进行分段。
    3、如果文档是问答格式类的，则将问题和答案分到同一段。
    4、如果文档且没有明显的段落，则可以分析语义，对有明显标题的部分，将标题和内容分在同一段。
    5、将语义相关性最高的语句分到同一个段落中。
    6、以一句话为单位，不能将一句话拆分到多个段落。
    7、每一个分段的内容尽量控制在1000字内，最多不能超过2000字，但本要求的优先级低于前5条。
    8、请以JSON格式输出分块内容，格式为：[{"keyword":"提取的关键字", "content":"分块的原文内容"}, ...]
    9、请直接给出答案，不需要思考和推理，也不用展示思考过程。\n
    #输入的原始文本# \n
    '''

    # 要读取Docx, 需要安装：pip install docx2txt
    documents = DocxReader().load_data("./docs/Cyber-Security.docx")
    # documents = UnstructuredReader().load_data("./docs/QA.txt")
    splitter = CustomSplitter(prompt=prompt)
    splits = splitter.get_nodes_from_documents(documents)
    # 查看分段内容，后续创建索引与检索等与之前的代码无差别
    for split in splits:
        print(split.get_content())
        print("===================")

    # index = VectorStoreIndex.from_documents(documents=documents, transformations=[splitter])
    # index.storage_context.persist(persist_dir="./dbstore/llamaindex-custom")
    #
    # storage_context = StorageContext.from_defaults(persist_dir='./dbstore/llamaindex-custom')
    # index = load_index_from_storage(storage_context)

    # retriever = index.as_retriever(similarity_top_k=10)
    # results = retriever.retrieve("第一阶段有哪些课程")
    # for result in results:
    #     print(result)

#     # context_str和query_str是内置变量，不能修改
#     prompt_tmpl = (
#         "以下是为模型提供的上下文信息：\n"
#         "------------------\n"
#         "{context_str}"
#         "\n---------------------\n"
#         "根据这些信息，请回答问题: {query_str}\n"
#         "如果您不知道的话，请回答不知道\n"
#     )
#     qa_prompt = Prompt(template=prompt_tmpl)
#     query_engine = index.as_query_engine(text_qa_template=qa_prompt, similarity_top_k=10)
#     response = query_engine.query("课程共有几个阶段？分别有什么重点内容？")
#     print(response)