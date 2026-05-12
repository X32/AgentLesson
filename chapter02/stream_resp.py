from fastapi import FastAPI, Request
import uvicorn
import json
import time
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
import uvicorn, os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# @app.post("/stream")
# def stream():
#     return StreamingResponse(handle_post_request())
#
# def handle_post_request():
#     for i in range(6):
#         print(i)
#         time.sleep(1)
#         # yield json.dumps({'type': i}) + '\n'
#         yield json.dumps({'x':i})


def stream_chat(question):
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
        # 使用生成器迭代输出每一个数据流
        yield json.dumps({"content":chunk.choices[0].delta.content}) + "\n"

@app.post("/stream")
def stream():
    return StreamingResponse(stream_chat("你好，你是谁？"), media_type="text/event-stream")

@app.get('/chat')
def chat(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html")

if __name__ == "__main__":
    uvicorn.run(app)