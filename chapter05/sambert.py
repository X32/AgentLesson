from fastapi import FastAPI, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn, time, dashscope, os
from dotenv import load_dotenv
from dashscope.audio.tts import SpeechSynthesizer

load_dotenv()
dashscope.api_key = os.getenv('Dashscope_API_Key')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse(request=request, name="sambert.html")

@app.post('/speech')
def speech(data: dict=Body()):
    result = SpeechSynthesizer.call(model='sambert-zhiqi-v1',
                                    text=data['content'],
                                    sample_rate=48000,
                                    format='mp3')
    if result.get_audio_data() is not None:
        with open('./static/sambert.mp3', 'wb') as f:
            f.write(result.get_audio_data())
    else:
        print('出现错误', result.get_response())
    return {"url": "/static/sambert.mp3"}   # 返回路径给前端

if __name__ == '__main__':
    uvicorn.run(app)