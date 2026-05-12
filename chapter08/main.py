import json

from fastapi import FastAPI, Request, Body, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from module import chat_llm, chat_llm_2, aes_encrypt, check_token, create_index
import uvicorn, time
from datetime import datetime
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
#     return StreamingResponse(chat_llm_2(content), media_type="text/event-stream")

# 为了保存对话记录，需要获取前端的user_token参数值
@app.post("/chat")
def chat(question: dict=Body()):
    content = question['content']
    user_token = question['user_token']
    return StreamingResponse(chat_llm_2(content, user_token), media_type="text/event-stream")

@app.post("/login")
def login(logins: dict = Body()):
    username = logins["username"]
    password = logins["password"]
    expiredTime = int(time.time()) + 60 * 60 * 24
    if username == "admin" and password == "Woniu.11":
        token = aes_encrypt(f"{username}|{password}|{expiredTime}")
        return {"message": "login-ok", "token": token, "username": username}
    else:
        return {"message": "login-fail"}

@app.post("/checklogin")
def checklogin(token: dict = Body()):
    token = token["token"]
    message = check_token(token)
    return message

# 渲染后台管理首页
@app.get("/admin")
def admin(request: Request):
    docinfos = json.load(open("dbstore/documents-info.json", encoding='utf-8'))
    return templates.TemplateResponse(request=request, name="admin.html", context={"docinfos": docinfos})

@app.post("/upload")
def upload(token: str = Form(), title: str = Form(), collection: str = Form(), file: UploadFile = File()):
    # Token检验
    if check_token(token)['message'] != "Token-OK":
        return "Token-Expired"

    # 读取文档名称和大小
    doc_file = file.file.read()
    suffix = file.filename.split(".")[-1]
    file_size = file.size

    # 判断文档类型是否正确
    allowed_type = ['md', 'txt', 'doc', 'docx', 'pdf']
    if not suffix in allowed_type:
        return "File-Type-Error"

    # 保存文档到static/docs目录下，可供后续用户下载
    filename = datetime.now().strftime(f"%Y%m%d_%H%M%S_%f.{suffix}")
    with open(f"static/docs/{filename}", "wb") as f:
        f.write(doc_file)

    # 调用module.py中的create_index来创建索引
    result = create_index(filename, suffix, title, file_size, collection)
    if result == "Create_Index_OK":
        return "Upload-Complete"

    return "Upload-Failed"

# 显示文档分段内容
@app.get("/section/{docname}")
def section(request: Request, docname: str):
    sections = json.load(open(f"dbstore/sections/{docname}.json", encoding='utf-8'))
    return templates.TemplateResponse(request=request, name="section.html", context={"sections": sections})

if __name__ == '__main__':
    uvicorn.run(app)