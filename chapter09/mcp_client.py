import json, os, asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('Dashscope_API_Key')
base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
server_url = "https://mcp.amap.com/sse?key=46644f43e3a56ce81f6f3633c5994c67"

class MCPClient:
    def __init__(self):
        self.sessions = []       # 存储服务器的会话及其上下文对象
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    # 初始化SSE服务器的连接，并获取可用工具列表。
    async def init_session(self):
        # 创建 SSE 客户端并进入上下文
        streams_context = sse_client(url=server_url)
        streams = await streams_context.__aenter__()
        session_context = ClientSession(*streams)
        session = await session_context.__aenter__()
        await session.initialize()

        # 存储会话及其上下文
        self.sessions = [session, session_context, streams_context]

    # 处理用户的自然语言查询，通过工具调用完成任务并返回结果。
    async def process_query(self, query: str):
        # 初始化消息列表
        messages = [{"role": "user", "content": query}]

        available_tools = []  # 收集所有可用工具
        session, _, _ = self.sessions   # 获取session对象
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

        # 向模型发送初始请求（带tools参数，非流式）
        response = await self.client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            tools=available_tools,
        )

        # 读取模型的响应
        message = response.choices[0].message

        # 明确了大模型返回的函数调用及参数值后，开始进行工具调用
        if message.tool_calls:
            # 一次可能存在多个函数调用的情况
            for tool in message.tool_calls:
                function_name = tool.function.name
                function_args = json.loads(tool.function.arguments)
                try:
                    result = await session.call_tool(function_name, function_args)
                    print(f"[调用工具 {function_name} 参数: {function_args}]，结果：{result}")
                    messages.append({"role": "user", "content": str(result.content)})
                except Exception as e:
                    print(f"调用工具 {function_name} 出错：{str(e)}")

        # 再次将MCP返回的结果添加给大模型进行二次请求
        response = await self.client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            stream=True
        )
        async for chunk in response:
            text = chunk.choices[0].delta.content
            if text:
                yield text


    # 清理所有会话和连接资源，确保无资源泄漏。
    async def cleanup(self):
        # 清空上下文和会话等对象，并断开与服务器的连接
        session, session_context, streams_context = self.sessions
        try:
            await session_context.__aexit__(None, None, None)
            await streams_context.__aexit__(None, None, None)
            await session.__aexit__(None, None, None)
        except:
            pass
        print("所有会话已清理。")

# 异步调用主函数
async def main():
    client = MCPClient()
    await client.init_session()   # 初始化并输出工具列表
    async for text in client.process_query("查询成都市环球中心附近酒店。"):
        print(text, end='')
    # await client.cleanup()        # 调用后必须清理

if __name__ == '__main__':
    asyncio.run(main())