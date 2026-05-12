import websockets, numpy as np
import json, face_recognition, cv2, asyncio
# 直接从之前的模块中导入考勤所需要函数
from pycheckin import check_faces

async def detect_image(websocket):
    try:
        while True:
            image_data = await websocket.recv()

            image_array = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            # 此处只考虑单张人脸的情况，先将人脸位置标注响应给前端
            locations = face_recognition.face_locations(frame)
            if len(locations) > 0:
                x = locations[0][3]
                y = locations[0][0]
                width = locations[0][1] - locations[0][3]
                height = locations[0][2] - locations[0][0]
                location = {"x": x, "y": y, "width": width, "height": height}
                await websocket.send(json.dumps(location))

                # 再对检测到的人脸进行比对和考勤，直接调用OpenCV版函数即可
                check_result = check_faces(frame)
                await websocket.send(json.dumps({"result": check_result}))

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