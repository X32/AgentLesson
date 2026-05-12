import websockets, os, dashscope, asyncio, wave, time, random
from dashscope.audio.asr import Recognition
from http import HTTPStatus
from dotenv import load_dotenv
load_dotenv()

dashscope.api_key = os.getenv('Dashscope_API_Key')

# 创建一个缓冲区来存储音频数据（二进制）
audio_buffer = bytearray()

# 调用Paraformer将音频文件转换为文字
async def transcribe(audio_file):
    content = ""
    try:
        recognition = Recognition(model='paraformer-realtime-v2',
                                  format='wav',
                                  sample_rate=16000,
                                  language_hints=['zh', 'en'],
                                  callback=None)
        result = recognition.call(audio_file)

        if result.status_code == HTTPStatus.OK:
            sentences = result.get_sentence()
            for sentence in sentences:
                content += sentence['text']
            print('识别结果：', content)
        else:
            print('出现错误: ', result.message)
    except:
        pass

    return content

# 将音频二进制文件保存为Wav文件
async def save_data(message):
    # 将新的音频数据添加到缓冲区
    audio_buffer.extend(message)

    # 当缓冲区达到64K时处理识别
    if len(audio_buffer) >= 64 * 1024:
        # 在临时目录下生成一个文件，并写入音频数据和参数
        time_stamp = time.strftime('%Y%m%d_%H%M%S')
        temp_wav_name = f"{time_stamp}_{random.randint(1, 1000)}.wav"
        temp_wav_path = f"./audio/{temp_wav_name}"
        # 使用wave库将二进制数据格式化为wav再进行保存
        with wave.open(temp_wav_path, 'wb') as wf:
            wf.setnchannels(1)   # 单通道
            wf.setsampwidth(2)   # 双位宽
            wf.setframerate(16000)  # 抽样频率
            wf.writeframes(bytes(audio_buffer))

        audio_buffer.clear()    # 清空缓冲区，以记录下一条数据

        return temp_wav_path    # 返回临时文件路径

# 实时读取客户端音频数据并进行识别
async def ws_handle(websocket):
    async for message in websocket:
        temp_wav_path = await save_data(message)
        content = await transcribe(temp_wav_path)
        await websocket.send(content)   # 发送识别的文字作为响应

# 定义WebSocket服务器和端口信息
async def main():
    server = await websockets.serve(ws_handle,"localhost",8765)
    print("WebSocket 服务器已启动，监听 ws://localhost:8765")
    # 保持服务器一直运行
    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
