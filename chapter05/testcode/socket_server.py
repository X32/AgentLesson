import websockets
import asyncio

# 定义一个异步函数用于处理前端请求和后续操作
async def echo(websocket):
    async for message in websocket:    # 遍历客户端的所有消息
        print(f"前端发送: {message}")
        await websocket.send(f"服务器回复: {message}")   # 发送响应

# 定义WebSocket服务器和端口信息
async def main():
    server = await websockets.serve(echo,"localhost",8765)
    print("WebSocket 服务器已启动，监听 ws://localhost:8765")
    # 保持服务器一直运行
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())