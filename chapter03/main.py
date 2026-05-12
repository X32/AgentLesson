from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from qa import qa
from recognize import recog
from generate import generate
import uvicorn
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
# 设置静态目录为static，并且在前端的引用路径为 /static
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(qa)
app.include_router(recog)
app.include_router(generate)

@app.get('/')
def chat(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html")

if __name__ == '__main__':
    uvicorn.run(app)