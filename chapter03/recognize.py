from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
import json, os, base64
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

recog = APIRouter()

# 图像识别通常为单次对话，可以不保存历史记录
@recog.post("/recognize")
def recognize_image(data: dict=Body()):
    # JS提交过来的Base64格式大致为：data:image/jpeg;base64,9j/4AAQSkZJRgA
    # 如果发送给千问VL图像识别模型，则可以直接发送
    # 如果要保存到本地，则需要提取其中的Base64字符串正文部分
    b64str = data['base64'].split(',')[1]

    def stream_chat():
        client = OpenAI(api_key=os.getenv("Dashscope_API_Key"),
                        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

        completion = client.chat.completions.create(
            model="qwen-vl-max-latest",
            messages=[
                {"role": "system","content": "你是一名专业的AI助手，可以帮助用户解答任何问题，也能以精准简洁的语言识别并描述出图像的内容。"},
                {"role": "user", "content": [{
                    "type": "image_url", "image_url": data['base64']
                },
                {"type": "text", "text": data['content']}]}
            ],
            stream=True
        )
        for chunk in completion:
            # 使用生成器迭代输出每一个数据流
            choice = chunk.choices[0].delta.content
            yield json.dumps({"content": choice}) + "\n"

    # 以流式响应的方式响应给前端
    return StreamingResponse(stream_chat(), media_type="text/event-stream")
