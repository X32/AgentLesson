# 利用Vosk进行语音唤醒，并调用Paraformer进行识别

import speech_recognition as sr
import vosk, json, time


mic = None
r = sr.Recognizer()
r.vosk_model = vosk.Model(model_path="D:/AIModels/vosk-model-small-cn-0.22")

# 定义一个循环程序
def loop():
    for i in range(5):
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)

def wake_up():
    while True:
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audioData = r.listen(source)
        said = r.recognize_vosk(audioData)
        content = json.loads(said)['text']
        if "你好" in content or "中国" in content:
            print("系统检测到你正在唤醒语音识别服务")
            loop()

if __name__ == '__main__':
    wake_up()

