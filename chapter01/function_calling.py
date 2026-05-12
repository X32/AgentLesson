import requests, os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

# 系统级提示词
system_prompt = """
	你是一名AI助手，具备函数调用的能力，但是如果提供的信息已经足够回答用户的问题，则不需要再进行函数调用。
	同时，请严格按照函数调用的方式进行处理，如果用户未提供函数所需参数，则必须询问，而不能自作主张。
"""

# 声明函数及参数说明，注意中文描述要尽量准确，便于大模型理解
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某个城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "中国的城市名称或区县的名称",
                    }
                },
                "required": ["city"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "往某个文件中写入内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "待写入的文件路径",
                    },
                    "content": {
                        "type": "string",
                        "description": "写入文件中的内容",
                    }
                },
                "required": ["filename", "content"]
            },
        }
    }
]

# 定义函数write_file用于写入内容
def write_file(filename, content):
    with open(f"D:/AITest/{filename}", "w", encoding="utf-8") as file:
        file.write(content)
    return f"文件{filename}写入成功"

# 定义函数用于通过高德天气接口查询天气
def get_weather(city):
    amap_api_key = "46644f43e3a56ce81f6f3633c5994c67"
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key={amap_api_key}&extensions=all"
    response = requests.get(url)
    return response.json()["forecasts"]

# 向DeepSeek发送请求，是否流式响应在调用时决定
def send_messages(messages):
    client = OpenAI(api_key=os.getenv("DeepSeek_API_Key"), base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=functions,   # 必须要传递此参数用于告诉大模型函数及参数定义情况
        stream=False
    )
    return response.choices[0].message

# 通过对模型的响应进行判断来决定是否调用函数
def invoke(content):
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": content}]
    message = send_messages(messages)
    print(message)
    # 响应在存在：function=Function(arguments='{"city":"北京"}', name='get_weather')

    # 如果响应中存在tool_calls不为空，则说明大模型返回了函数及参数，需要进行函数调用
    if message.tool_calls:
        # 提取函数调用信息：函数名称和函数的参数
        func_name = message.tool_calls[0].function.name
        func_args = eval(message.tool_calls[0].function.arguments)  # 将参数字符串解析为字典

        func = globals()[func_name]  # 将函数名称字符串转换为函数体
        func_response = func(**func_args)  # 利用**将字典对象解析为参数

        # 将查询到的天气信息再次与用户提问一同提交给大模型进行分析
        messages = [
            {"role": "user", "content": f"请基于该信息：{func_response}\n来回答以下问题，请直接回答问题，不需要再进行函数调用，直接返回结果\n{content}"}]
        message = send_messages(messages)
        print(message.content)  # 得到最终的穿衣建议
    else:
        # 如果没有函数调用，直接输出 DeepSeek 的回复
        print("无函数调用，模型回复内容为:", message.content)

if __name__ == '__main__':
    content = "明天去北京出差适合穿什么衣服？"
    invoke(content)
    content = "请在Test2.txt文件中写入内容：你好，蜗牛学苑！"
    invoke(content)