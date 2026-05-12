from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import StorageContext, Settings, Prompt
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.readers.file import MarkdownReader, PDFReader, DocxReader, UnstructuredReader
from llama_index.core.node_parser import MarkdownNodeParser, SentenceSplitter
import json, chromadb, os, time, requests
from datetime import datetime
from ollama import Client
from func_calling import new_customer, functions
from dotenv import load_dotenv
load_dotenv()

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from binascii import a2b_hex

key = os.getenv("Token_AES_Key").encode()
iv = os.getenv("Token_AES_IV").encode()

# 定义词嵌入模型和对话模型
base_url = "http://192.168.55.200:11434"
Settings.embed_model = OllamaEmbedding(base_url=base_url, model_name="qwen3:8b")
Settings.llm = Ollama(base_url=base_url, model="qwen3:8b", thinking=False)

# 加载索引
chroma_client = chromadb.PersistentClient("dbstore/chroma")
chroma_collection = chroma_client.get_or_create_collection("Woniu-Collection")
vectorstore = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store=vectorstore)


# AI对话,重点在于提示词的处理，添加联网搜索功能
def chat_llm(question):
    search_string = aliyun_search(question)

    # 注意此处不能使用 f 来拼接搜索结果，因为 {context_str} 是模板变量，代码无法解析
    prompt_tmpl = """
        蜗牛学苑是一家知名的IT培训机构，你现在扮演的是一名专业的在线客服，
        可以回答用户提出来的任何关于培训的相关问题。在线客服的职责是解答完用户的问题后，
        获取用户的联系方式（手机号或微信号），你需要在每次回答的最后向用户索要联系方式，
        这并不违背法律和商业伦理，同时，也可以询问用户是否对本次回答感到满意，
        如果满意就留下联系方式，如果不满意则回复抱歉并让用户继续提问。\n
        另外，请根据提供的上下文内容来回答问题，如果某些问题没有答案，则可以基于你自已的理解来回复用户，
        让用户感觉到你的专业，但是不能胡乱编造，尽量以文档中提及的内容为基准进行扩展，
        或根据行业的公开数据为回答基准。请务必在任何时候都将自已代入角色中，
        回答问题时尽量以“蜗牛学苑”或“我们”来称呼自已，最好不使用“文档中提到”这类文字。
        由于你是一名专业的在线客服，所以在回答用户问题时，
        一定要挑选重点，简明扼要，每次的回答尽量控制在200字以内即可。上下文内容为:\n
        -----------------------------------
        {context_str} 
        -----------------------------------
        \n\n""" + search_string + "\n\n 用户的提问内容为: {query_str}"""

    qa_prompt = Prompt(template=prompt_tmpl)
    chat = index.as_chat_engine(text_qa_template=qa_prompt, similarity_top_k=10)
    result = chat.stream_chat(question)
    for chunk in result.response_gen:
        yield json.dumps({"content": chunk}) + "\n"

# 阿里云搜索服务，返回搜索结果字符串
def aliyun_search(question):
    url = "http://default-w4yy.platform-cn-shanghai.opensearch.aliyuncs.com/v3/openapi/workspaces/default/web-search/ops-web-search-001"
    api_key = os.getenv('Aliyun_Search_Key')
    header = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    # way=full：使用大模型对搜索结果进行评判和过滤，默认为：fast，不过滤
    # content_type=summary：对网页内容的文本进行摘要，默认为：snippet，简短描述
    data = {"query": f"蜗牛学苑 {question}", "top_k": 5, "way": "full", "content_type": "summary"}
    resp = requests.post(url, headers=header, json=data)

    # print("Aliyun Search: ", resp.text)

    if "result" in resp.json():
        list = resp.json()['result']['search_result']
        content = ""
        for line in list:
            content += line['content'] + '\n\n'
        return content
    else:
        return ""

# 为AI对话添加联网搜索功能，联系人自动提醒功能，对话记录保存功能
def chat_llm_2(question, user_token):
    # 先检索出相似度较高的15条文档，并将其拼接为字符串
    retriever = index.as_retriever(similarity_top_k=15)
    results = retriever.retrieve(question)

    context_string = ""
    for result in results:
        context_string += result.text + '\n\n'

    # 再获取5条与问题相关的搜索结果
    search_string = aliyun_search(question)

    prompt = f"""
        蜗牛学苑是一家知名的IT培训机构，你现在扮演的是一名专业的在线客服，
        可以回答用户提出来的任何关于培训的相关问题。在线客服的职责是解答完用户的问题后，
        获取用户的联系方式（手机号或微信号），你需要在每次回答的最后向用户索要联系方式，
        如果获取到用户的联系方式，请尝试返回Function Calling去调用函数new_customer，并提取其参数。
        同时回复给用户以下内容：您的联系方式已告知我们的同事，会尽快与您联系，感谢您的信任。
        这并不违背法律和商业伦理，同时，也可以询问用户是否对本次回答感到满意，
        如果满意就留下联系方式，如果不满意则回复抱歉并让用户继续提问。\n
        另外，请根据提供的上下文内容来回答问题，如果某些问题没有答案，则可基于你自已的理解来回复用户，
        让用户感觉到你的专业，但是不能胡乱编造，尽量以文档中提及的内容为基准进行扩展，
        或根据行业的公开数据为回答基准。请务必在任何时候都将自已代入角色中，
        回答问题时尽量以“蜗牛学苑”或“我们”来称呼自已，最好不使用“文档中提到”这类文字。
        由于你是一名专业的在线客服，所以在回答用户问题时，
        一定要挑选重点，简明扼要，每次的回答尽量控制在200字以内即可。上下文内容为:\n
        -----------------------------------
        {context_string} \n\n
        {search_string} \n\n
        -----------------------------------
        用户的提问内容为: {question}"""

    # 实例化Ollama客户端与进行第一次非流式调用，来确定是否需要调用函数
    client = Client(host=base_url)
    messages = [{'role': 'system','content': "你是一名来自蜗牛学苑的专业客服顾问，同时具备函数调用的能力。"},
            {'role': 'user','content': prompt}]

    # stream=False, tools=functions，且本次调用的提示词只包含用户的内容，无检索结果
    completion = client.chat(model='qwen3:8b', stream=False, think=False, messages=[{'role': 'user','content': question}], tools=functions)

    # print(completion)    # 调试时可输出completion的层次结构

    # 从非流式响应中确认是否存在函数调用，存在则调用
    tool_calls = completion.message.tool_calls

    if tool_calls:
        func_name = tool_calls[0].function.name
        func_args = tool_calls[0].function.arguments
        func = globals()[func_name]
        result = func(**func_args)     # 函数调用
        if result == "Mail-Sent":
            # 如果获取到联系方式并且通知成功，则重新定义提示词，以覆盖之前的大段提示词
            messages = [{"role":"user", "content": "请回复用户：您的联系方式已告知我们的同事，会尽快与您联系，感谢您的信任。"}]

    # 无论是否存在函数调用，都要正常回复给用户
    # stream = client.chat(model='qwen3:8b', messages=messages, stream=True, think=False)
    # for chunk in stream:
    #   yield json.dumps({"content": chunk.message.content}) + "\n"

    # 为对话添加对话记录功能
    history = {"user_token": user_token, "question": question}
    stream = client.chat(model='qwen3:8b', messages=messages, stream=True, think=False)
    reply = ""
    for chunk in stream:
        content = chunk.message.content
        yield json.dumps({"content": content}) + "\n"
        reply += content

    history["reply"] = reply
    save_history(history)    # 调用函数保存对话记录

# 保存对话历史记录
def save_history(history):
    user_token = history['user_token']
    question = history['question']
    reply = history['reply']

    # 确认是否要在history目录下创建当天日期的目录
    today = time.strftime("%Y%m%d")
    if not os.path.exists(f"history/{today}"):
        os.mkdir(f"history/{today}")

    # 如果不存在该user_token对应的JSON，则新建文件并保存第一条记录
    if not os.path.exists(f"history/{today}/{user_token}.json"):
        with open(f"history/{today}/{user_token}.json", 'w', encoding="utf-8") as file:
            # 构建第一条JSON记录，并且保存为列表，否则后续JSON无法添加
            qa = {"question": question, "reply": reply}
            json.dump([qa], file, ensure_ascii=False)
    else:
        # 如果已经存在，则先读取，再追加，再覆盖的方式保存JSON
        with open(f"history/{today}/{user_token}.json", 'r', encoding="utf-8") as file:
            data = json.load(file)
            data.append({"question": question, "reply": reply})

        with open(f"history/{today}/{user_token}.json", 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)


# 读取文档、文档分段、保存分段内容、保存文档信息、创建索引
def create_index(file_name, suffix, title, file_size, collection):
    file_path = f"static/docs/{file_name}"
    # 如果要实现分段查看，则需要获取到分段后的内容，并且将其保存到以文件名命名的JSON中
    if suffix == "md":
        documents = MarkdownReader().load_data(file=file_path)
        splitter = MarkdownNodeParser()
        nodes = splitter.get_nodes_from_documents(documents)
        # 保存文档分段内容
        save_sections(file_name, nodes)
    elif suffix == "pdf":
        documents = PDFReader().load_data(file=file_path)
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        nodes = splitter.get_nodes_from_documents(documents)
        save_sections(file_name, nodes)
    elif suffix == "docx" or suffix == "doc":
        documents = DocxReader().load_data(file=file_path)
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        nodes = splitter.get_nodes_from_documents(documents)
        save_sections(file_name, nodes)
    elif suffix == "txt":
        documents = UnstructuredReader().load_data(file=file_path)
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        nodes = splitter.get_nodes_from_documents(documents)
        save_sections(file_name, nodes)

    # 以JSON来保存文档原始信息，用以在页面上显示文档数据
    # 需要提前创建好documents-info.json文件，并且里面添加[]，确保能够读取到正确的JSON列表
    docinfo = {"docname": file_name, "doctitle": title,  "filesize": file_size,
               "collection": collection, "createtime": time.strftime("%Y-%m-%d %H:%M:%S")}
    docinfos = json.load(open("dbstore/documents-info.json", encoding="utf-8"))
    docinfos.append(docinfo)
    json.dump(docinfos, open("dbstore/documents-info.json", "w", encoding="utf-8"), ensure_ascii=False)

    # 根据分段内容来创建索引
    chroma_client = chromadb.PersistentClient("dbstore/chroma")
    chroma_collection = chroma_client.get_or_create_collection(collection)
    vectorstore = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vectorstore)
    index = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context, transformations=[splitter])
    index.set_index_id(file_name)


    return "Create_Index_OK"

# 保存文档分段内容，每一份文档对应一个JSON文件，里面是文档分段列表
def save_sections(filename, nodes):
    sections = []
    for node in nodes:
        sections.append(node.get_content())
    json.dump(sections, open(f"dbstore/sections/{filename}.json", "w", encoding="utf-8"), ensure_ascii=False)


# 加密登录信息，并返回十六进制的Token
def aes_encrypt(source):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(source.encode(), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return encrypted.hex()

# 对Token进行解密，获取到原始明文
def aes_decrypt(encrypted):
    decipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = decipher.decrypt(a2b_hex(encrypted))
    decrypted = unpad(decrypted_padded, AES.block_size)
    return decrypted.decode()

# 此处Token的原文为用户信息，以|分隔：username|password|expiredtime
def check_token(token):
    timestamp = int(time.time())
    try:
        decrypted = aes_decrypt(token)
        temp_list = decrypted.split("|")
        expiredTime = temp_list[2]
        if timestamp > int(expiredTime):
            return {"message": "Token-Expired"}
        else:
            return {"message": "Token-OK", "username": temp_list[0]}
    except:
        return {"message": "Token-Error"}