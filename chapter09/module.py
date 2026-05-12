import json, os, dashscope
from datetime import datetime
from dashscope.audio.tts import SpeechSynthesizer
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

dashscope.api_key = os.getenv('Dashscope_API_Key')

# 用于保存对话的上下文记忆功能
messages = [{
    "role": "system",
    "content": "你是一名专业的导游，精通世界各地的景点、货币、和语言等知识，也非常擅长帮助用户规律旅游路线等。"
}]

def chat_llm(content):
    messages.append({"role": "user", "content": content})
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


# AI识图，无聊天记忆功能
def chat_image(question):
    image_base64 = question['image']
    content = question['content']
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_base64
                    },
                },
                {"type": "text", "text": content},
            ],
        },
    ]
    client = OpenAI(api_key=os.getenv("Dashscope_API_Key"),
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",
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

def translate(content):
    prompt = f"""
    您是一位精通「源文本语言」与「目标语言」文化和语言的翻译专家。\n
    # User prompt
    源本文: {content} \n
    ## 翻译要求:
    1.忠实于"源文本"，确保每个句子都得到准确且流畅的翻译。
    2.大额数字的翻译需准确无误，符合简体中文的表达习惯。
    3.翻译时，应避免使用生词或生僻词，尽量使用常用词。
    4.翻译时，应避免使用过于复杂的句式，尽量使用简单句。
    5.如果源文本是中文，则将其翻译为英文，如果源文本是英文或其他语言，则将其翻译为中文。
    ##任务:
    1.仔细研究并深入理解"源文本"的内容、上下文、语境、情感以及和目标语言的文化细微差异。
    2.根据「翻译要求」将"源文本"准确翻译为出来。
    3.确保翻译对目标受众来说准确、自然、流畅，必要时可以根据需要调整表达方式以符合文化和语言习惯。
    注意:不要输出任何额外的内容，只能输出翻译内容。这一点非常关键。
    """
    message = [{"role": "user", "content": prompt}]
    client = OpenAI(api_key=os.getenv("Dashscope_API_Key"),
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=message,
        stream=True,
        stream_options={"include_usage": False}
    )
    for chunk in completion:
        choice = chunk.choices[0].delta.content
        yield json.dumps({"content": choice}) + "\n"


def speak_sambert(content):
    filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f.mp3")
    result = SpeechSynthesizer.call(model='sambert-zhiqi-v1',  # 音色
                                text=content,
                                sample_rate=48000,    # 频率
                                format='mp3')
    if result.get_audio_data() is not None:
        with open(f'static/voices/{filename}', 'wb') as f:
            f.write(result.get_audio_data())
    else:
        print('出现错误', result.get_response())

    return filename