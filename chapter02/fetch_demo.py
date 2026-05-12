from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/hello")
def index() -> str:
    return HTMLResponse("<h1>Hello World</h1>")

@app.post("/login")
def login(username: str=Form(), password: str=Form()) -> dict:
    if username == "woniu" and password == "123456":
        return {"message": "登录成功"}
    else:
        return {"message": "登录失败"}

@app.get('/fetch')
def fetch(request: Request):
    return templates.TemplateResponse(request=request, name="fetch.html")

if __name__ == '__main__':
    uvicorn.run(app)