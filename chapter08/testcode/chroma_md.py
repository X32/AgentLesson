# 对MD文档进行分段操作并完成AI对话

import chromadb, re
from ollama import Client
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

# 定义词嵌入模型
ollama_url="http://192.168.55.200:11434"
ollama_ef = OllamaEmbeddingFunction(url=ollama_url, model_name="qwen3:8b")

class MyEmbeddingFunction(EmbeddingFunction):
    def __init__(self, **kwargs):
        pass

    def __call__(self, texts: Documents) -> Embeddings:
        return ollama_ef.embed_with_retries(texts)

chroma_client = chromadb.PersistentClient("./dbstore/chroma")

# 如果存在Collection就直接get,否则创建
collection = chroma_client.get_or_create_collection(name="mycollection", embedding_function=MyEmbeddingFunction())


# 按MD的层次 ##, ### 等进行简单分段处理
def split_md(file_path):
    # 读取文件内容
    with open(file_path, mode='r', encoding='utf-8') as file:
        content = file.read()

    # 此处使用正则表达式re的split方法,可以一次指定多个分隔符
    results = re.split("#####|####|###|##", content)
    # 对于文字较少的内容,直接将其过滤掉(可选)
    sections = []
    for result in results:
        if len(result) > 10:
            sections.append(result)

    return sections

# 添加文档并创建索引
def create_index(file_path):
    sections = split_md(file_path)
    ids = [f"id_{i}" for i in range(1, len(sections) + 1)]
    collection.add(
        documents=sections,
        ids=ids
    )

# 相似度查询
def query_index(question, top_k=30):
    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )
    # 提取查询结果中的文档内容列表
    return results['documents'][0]

# AI大模型对话
def chat_llm(question):
    # 将所有查询到的文档用换行符拼接为字符串
    contexts = "\n\n\n".join(query_index(question))

    prompt = f"""请基于以下已知信息，简洁和专业的来回答用户的问题。已知信息内容为：\n
    ---------------------\n
    {contexts} \n
    ---------------------\n
    请根据这些信息，请回答问题: {question} \n
    如果你不知道如何回答该问题话，请回答不知道 \n """

    client = Client(host=ollama_url)
    messages=[{'role': 'user','content': prompt}]
    stream = client.chat(model='qwen3:8b', messages=messages, stream=True, think=False)

    for chunk in stream:
        print(chunk.message.content, end='', flush=True)


if __name__ == '__main__':
    # create_index("./docs/WoniuAI-V6.md")
    # chat_llm("可以学会AI这套课程吗？")
    chat_llm("AI课程分哪几个阶段")