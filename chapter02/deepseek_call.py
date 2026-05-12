from fastapi import FastAPI, Form, Request, Body
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
import uvicorn, os, json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# @app.post('/chat')
# def chat(question: str=Form()):
#     client = OpenAI(api_key=os.getenv("DeepSeek_API_Key"),
#                     base_url="https://api.deepseek.com")
#
#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant"},
#             {"role": "user", "content": question},
#         ],
#         stream=False
#     )
#     return response


# 定义接口，并将生成器输出封装到响应中，此处建议使用异步通信
# 前端的请求参数建议设置为JSON格式，如{"content": "你好"}
@app.post("/stream")
def stream_chat(question: dict=Body()):
    # 读取JSON参数的值
    question = question['content']

    # 定义大模型对话函数，同样建议使用异步通信
    def stream_chat():
        client = OpenAI(api_key=os.getenv("DeepSeek_API_Key"),
                        base_url="https://api.deepseek.com")

        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": question},
            ],
            stream=True
        )
        for chunk in completion:
            # 使用生成器迭代输出每一个数据流]
            choice = chunk.choices[0].delta.content
            yield json.dumps({"content":choice}) + "\n"

    # 以流式响应的方式响应给前端
    return StreamingResponse(stream_chat(), media_type="text/event-stream")

@app.get('/chat')
def chat(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html")


if __name__ == '__main__':
    uvicorn.run(app)