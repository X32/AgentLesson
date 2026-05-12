from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# 定义一个Get请求的接口，并返回一个HTML页面
@app.get("/")
def index() -> str:
    return HTMLResponse("<h1>Hello World</h1>")

# 定义一个Post请求的接口，模拟表单登录验证，并返回一个JSON
# 其中Form()表示从表单发送的常规的Post请求正文，
# 即：Content-Type: application/x-www-form-urlencoded
@app.post("/login")
def login(username: str=Form(), password: str=Form()) -> dict:
    if username == "woniu" and password == "123456":
        return {"message": "登录成功"}
    else:
        return {"message": "登录失败"}



# 在开发环境中进行调试，定义端口号为8000
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)