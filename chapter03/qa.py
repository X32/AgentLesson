from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
import json, os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from module import aliyun_search
from func_calling import send_email, functions

qa = APIRouter()

messages = [{
    "role": "system",
    "content": "你是一名专业的AI助手，可以帮助用户解答任何问题。"
}]

# 定义接口，并将生成器输出封装到响应中
@qa.post("/stream")
def stream(question: dict=Body()):
    # 读取JSON参数的值
    content = question['content']
    search = question['search']

    if search == True:
        search_result = aliyun_search(content)
        # print(search_result)
        message = {"role": "user", "content": f"请使用以下内容:\n{search_result}\n，并基于用户的提问：\n{content}\n来进行回答。"}
    else:
        message = {"role": "user", "content": content}

    # 增加函数调用的功能，让大模型理解用户的提问后返回函数调用的声明
    def check_func_call(message):
        messages.append(message)
        client = OpenAI(api_key=os.getenv("Dashscope_API_Key"),
                        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            stream=False,     # 函数调用不能与流式响应同时处理
            tools=functions
        )

        return completion.choices[0].message

    # stream_chat中不再运行messages.append(message)
    def stream_chat():
        # messages.append(message)
        # print(messages)
        client = OpenAI(api_key=os.getenv("Dashscope_API_Key"),
                        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            stream=True,
            stream_options={"include_usage": False}
        )
        # 定义变量reply用于保存本次回复内容，以便于实现聊天记忆功能
        reply = ""
        for chunk in completion:
            # 使用生成器迭代输出每一个数据流
            choice = chunk.choices[0].delta.content
            reply += choice
            yield json.dumps({"content": choice}) + "\n"
        # 循环结束后，将AI回复也添加到messages中
        messages.append({"role": "assistant", "content": reply})

    # 首先调用check_func_call，确认是否有函数调用
    # 如果有，则进行函数调用，并让大模型返回一个函数调用的结果给用户
    # 如果不存在函数调用的情况，则直接将用户的提问交给stream_chat来完成
    output = check_func_call(message)
    if output.tool_calls:
        func_name = output.tool_calls[0].function.name
        func_args = eval(output.tool_calls[0].function.arguments)
        func = globals()[func_name]
        result = func(**func_args)
        messages.append({"role": "user", "content": f"请将以下内容直接回复给用户: {result}"})
    else:
        messages.append(message)   # 此处已经添加用户问题，所以stream_chat中不再添加

    return StreamingResponse(stream_chat(), media_type="text/event-stream")