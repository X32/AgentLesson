from fastapi import FastAPI, Request, Body, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from module import chat_llm, chat_image, translate, speak_sambert
from mcp_client import MCPClient
import uvicorn, time, json
from aiohttp import web
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
def chat(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html")

# 定义接口，并将生成器输出封装到响应中
# @app.post("/chat")
# def chat(question: dict=Body()):
#     content = question['content']
#     return StreamingResponse(chat_llm(content), media_type="text/event-stream")


# 错误的处理方案
# @app.post("/chat")
# async def chat(question: dict=Body()):
#     content = question['content']
#     mcpclient = MCPClient()
#     await mcpclient.init_session()
#     return StreamingResponse(mcpclient.process_query(content), media_type="text/event-stream")
#     await mcpclient.cleanup()


# 正确的处理方案：异步内部函数
@app.post("/chat")
def chat(question: dict=Body()):
    content = question['content']

    # 定义异步内部函数用于调用MCPClient
    async def mcp_talk():
        mcpclient = MCPClient()
        await mcpclient.init_session()
        async for chunk in mcpclient.process_query(content):
            yield json.dumps({"content": chunk}) + "\n"
        await mcpclient.cleanup()

    # 流式响应
    return StreamingResponse(mcp_talk(), media_type="text/event-stream")


# 将前端传输来的图片的Base64编码与提示词一并交由对话函数处理
@app.post("/image")
def chat(question: dict=Body()):
    return StreamingResponse(chat_image(question), media_type="text/event-stream")

@app.post("/translate")
def chat(question: dict=Body()):
    content = question['content']
    return StreamingResponse(translate(content), media_type="text/event-stream")

@app.post("/speak")
def chat(question: dict=Body()):
    content = question['content']
    filename = speak_sambert(content)
    return {"filename": filename}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)