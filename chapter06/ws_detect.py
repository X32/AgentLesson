import websockets, numpy as np
import json, face_recognition, cv2, asyncio

async def detect_image(websocket):
    try:
        # 服务器端接收消息可以是 async for message in websocket:
        # 此时，接收到的内容则为message，第五章使用此方法
        # 也可以使用while True，再await websocket.recv()来接收消息
        while True:
            # 接收二进制图像数据
            image_data = await websocket.recv()

            # 将接收到的图像数据进行转码变成可用类型
            image_array = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            locations = face_recognition.face_locations(frame)
            location_list = []
            for location in locations:
                # location的值为（top, right, bottom, left），以左上为原点可对应为（y1, x2, y2, x1)
                # top表示最上方的Y坐标，bottom表示最下方的Y坐标，right和left则表示X方向坐标
                # 将其转换为左上角的（x,y)坐标和矩形的宽度和高度，以便于前端绘制DIV
                x = location[3]  # left的坐标即为 x
                y = location[0]  # top的坐标即为 y
                width = location[1] - location[3]  # right-left为宽度
                height = location[2] - location[0]  # bottom-top为高度
                location_list.append({"x": x, "y": y, "width": width, "height": height})
            # 将符合前端需要的所有人脸的坐标和宽度高度响应给前端
            await websocket.send(json.dumps(location_list))

    except websockets.ConnectionClosed:
        print("WS连接关闭.")
    except Exception as e:
        print(f"出现错误: {e}")

async def main():
    server = await websockets.serve(detect_image, "localhost", 8765)
    print("WebSocket server started at ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())