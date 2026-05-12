import asyncio
import json
from mcp import ClientSession
from mcp.client.sse import sse_client
from openai import AsyncOpenAI

from dotenv import load_dotenv
load_dotenv()

class MCPClient:
    def __init__(self):
        self.sessions = []       # 存储服务器的会话及其上下文
        self.model_name = "deepseek-chat"
        self.server_url = "https://mcp.amap.com/sse?key=46644f43e3a56ce81f6f3633c5994c67"
        # self.server_url = "http://localhost:8000/sse"
        self.client = AsyncOpenAI(base_url="https://api.deepseek.com", api_key="sk-27eb212db04e480fb0f0f75c6e390af0")

    # 初始化SSE服务器的连接，并获取可用工具列表。
    async def init_session(self):
        # 创建 SSE 客户端并进入上下文
        streams_context = sse_client(url=self.server_url)
        streams = await streams_context.__aenter__()
        session_context = ClientSession(*streams)
        session = await session_context.__aenter__()
        await session.initialize()

        # 存储会话及其上下文
        self.sessions = [session, session_context, streams_context]

        # 获取工具列表并建立映射
        response = await session.list_tools()
        for tool in response.tools:
            print(tool)

    # 清理所有会话和连接资源，确保无资源泄漏。
    async def cleanup(self):
        session, session_context, streams_context = self.sessions
        try:
            await session_context.__aexit__(None, None, None)  # 退出会话上下文
            await streams_context.__aexit__(None, None, None)  # 退出 SSE 流上下文
        except:
            pass
        print("所有会话已清理。")

    # 处理用户的自然语言查询，通过工具调用完成任务并返回结果。
    async def process_query(self, query: str):
        # 初始化消息列表
        messages = [{"role": "user", "content": query}]

        available_tools = []  # 收集所有可用工具
        session, _, _ = self.sessions
        response = await session.list_tools()
        for tool in response.tools:
            # 构造满足Function Calling规范的函数声明
            function = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            available_tools.append(function)

        # 向模型发送初始请求（带tools参数）
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=available_tools,
        )

        # 读取模型的响应
        message = response.choices[0].message
        print(message)
        # 结果：ChatCompletionMessage(content='', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_0_d7f56950-d8d8-451d-8528-b0a0e0fd8dbd', function=Function(arguments='{"city":"成都"}', name='maps_weather'), type='function', index=0)])

        # 明确了大模型返回的函数调用及参数值后，开始进行工具调用
        if message.tool_calls:
            results = []
            # 一次可能存在多个函数调用的情况
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                try:
                    result = await session.call_tool(function_name, function_args)
                    print(f"[调用工具 {function_name} 参数: {function_args}]，结果：{result}")
                    results.append(result.content)
                    messages.append({"role": "assistant", "content": str(result.content)})
                except Exception as e:
                    print(f"调用工具 {function_name} 出错：{str(e)}")

            # 再次将MCP返回的结果添加给大模型进行二次请求
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=available_tools,
                stream=True
            )
            async for chunk in response:
                text = chunk.choices[0].delta.content
                if text:
                    # print(text, end='')  # 直接打印方式
                    yield text             # 异步生成器方式

async def main():
    client = MCPClient()
    try:
        await client.init_session()
        # await client.process_query("查询成都市明天的天气及天府二街附近酒店。")  # 直接打印
        async for text in client.process_query("查询成都市明天的天气及酒店。"):   # 异步生成器调用
            print(text, end='')
    except:
        pass
    finally:
        await client.cleanup()

if __name__ == '__main__':
    asyncio.run(main())