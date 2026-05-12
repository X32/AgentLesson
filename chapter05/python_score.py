import tkinter as tk
from tkinter import *
import os, time, re, threading, pyttsx3
import speech_recognition as sr
import vosk, json, dashscope, pyaudio
from dashscope.audio.asr import *
from dotenv import load_dotenv
load_dotenv()

mic = None
stream = None
dashscope.api_key = os.getenv('Dashscope_API_Key')


# 实例化与加载Vosk模型
r = sr.Recognizer()
r.vosk_model = vosk.Model(model_path=r"D:\AIModels\vosk-model-small-cn-0.22")

# 定义Paraformer的回调类
class Callback(RecognitionCallback):
    def on_open(self) -> None:
        global mic
        global stream
        print('开始语音识别')
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True)

    def on_complete(self) -> None:
        print('语音识别完成.')  # recognition completed

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if RecognitionResult.is_sentence_end(sentence):
            # 当识别到文字时，调用do_score()进行语音记分
            print('识别结果为: ', sentence['text'])
            do_score(sentence['text'])

def start_paraformer():
    try:
        callback = Callback()
        recognition = Recognition(model='paraformer-realtime-v1',
                                  format='pcm',
                                  sample_rate=16000,
                                  disfluency_removal_enabled=True,
                                  callback=callback)

        recognition.start()

        start_time = time.time()   # 开始计时，4秒后停止
        while True:
            if stream:
                data = stream.read(3200, exception_on_overflow=False)
                recognition.send_audio_frame(data)
            else:
                break

            end_time = time.time()

            # 延迟4秒后停止识别
            duration = int(end_time - start_time)
            if duration >= 4:
                recognition.stop()
    except:
        pass

def vosk_wakeup():
    while True:
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audioData = r.listen(source)

        said = r.recognize_vosk(audioData)
        text = json.loads(said)['text']
        if "你好" in text or "中国" in text:
            print("系统检测到你正在唤醒语音识别服务")
            pyttsx3.speak("在呢")
            start_paraformer()   # 4秒结束后继续等待唤醒

def start_game():
    pyttsx3.speak("好的，开始本局")
    # 点击开始按钮时，用一个子线程来启动语音唤醒，以免Vosk阻塞界面其他操作
    threading.Thread(target=vosk_wakeup).start()


# 定义关键数字字典，便于识别时提取数字
voice_dict = {"一": 1, "1": 1, "两":2, "二": 2, "2":2, "三":3, "3":3, "四":4, "4":4, "五":5, "5":5,
              "六":6, "6":6, "七":7, "7":7, "八":8, "8":8, "九": 9, "9": 9, "十":10, "10":10}

# 语音记分操作，进行关键字模糊匹配
def do_score(text):
    if "红" in text:
        if "加" in text or "家" in text:
            for k, v in voice_dict.items():
                if k in text:
                    red_plus(v)
                    pyttsx3.speak(f"好的，红队加{v}分")
        elif "减" in text or "见" in text:
            for k, v in voice_dict.items():
                if k in text:
                    red_minus(v)
                    pyttsx3.speak(f"好的，红队减{v}分")

    elif "蓝" in text or "男" in text:
        if "加" in text or "家" in text:
            for k, v in voice_dict.items():
                if k in text:
                    blue_plus(v)
                    pyttsx3.speak(f"好的，蓝队加{v}分")
        elif "减" in text or "见" in text:
            for k, v in voice_dict.items():
                if k in text:
                    blue_minus(v)
                    pyttsx3.speak(f"好的，蓝队减{v}分")

    elif "撤消" in text or "撤销" in text:
        undo_score()

    elif "结束" in text:
        end_game()
        pyttsx3.speak(f"好的，结束本局。")

def red_plus(score):
    old = int(entry_red.get())    # 获取现有得分
    entry_red.delete(0, 5)   # 清空全部值
    entry_red.insert(0, old + score)   # 给文本框赋新值
    update_log(f"红队 加 {score} 分")   # 更新日志

def red_minus(score):
    old = int(entry_red.get())
    entry_red.delete(0, 5)
    entry_red.insert(0, old - score)
    update_log(f"红队 减 {score} 分")

def blue_plus(score):
    old = int(entry_blue.get())
    entry_blue.delete(0, 5)
    entry_blue.insert(0, old + score)
    update_log(f"蓝队 加 {score} 分")

def blue_minus(score):
    old = int(entry_blue.get())
    entry_blue.delete(0, 5)
    entry_blue.insert(0, old - score)
    update_log(f"蓝队 减 {score} 分")

def update_log(content):
    now = time.strftime("%H:%M:%S")
    text_log.insert(INSERT, f"{now}: {content}\n")
    text_log.focus_force()
    text_log.see(END)    # 滚动到最末尾
    text_log.update()    # 更新日志记录框
    print(f"{now}: {content}")


def undo_score():
    # 获取全部日志记录,1.0表示开始位置，end表示结束
    score_log = text_log.get(1.0, "end")
    last_log = score_log.split("分")[-2]
    log_fields = last_log.split()
    print(log_fields)

    if log_fields[1] == "红队" and log_fields[2] == "加":
        red_minus(int(log_fields[3]))
    elif log_fields[1] == "红队" and log_fields[2] == "减":
        red_plus(int(log_fields[3]))
    elif log_fields[1] == "蓝队" and log_fields[2] == "加":
        blue_minus(int(log_fields[3]))
    elif log_fields[1] == "蓝队" and log_fields[2] == "减":
        blue_plus(int(log_fields[3]))

    pyttsx3.speak("好的，得分已撤销")

def end_game():
    red_result_old = int(label_red_score["text"])
    blue_result_old = int(label_blue_score["text"])
    if int(entry_red.get()) > int(entry_blue.get()):
        red_result = red_result_old + 1
        label_red_score["text"] = red_result
    else:
        blue_result = blue_result_old + 1
        label_blue_score["text"] = blue_result

    entry_red.delete(0, 5)
    entry_red.insert(0, "0")
    entry_blue.delete(0, 5)
    entry_blue.insert(0, "0")

    update_log("本局比赛结束")
    pyttsx3.speak("本局比赛结束")


# 界面绘制
root = tk.Tk()    # 实例化tkinter，作为主容器使用
root.title("智能语音记分牌")
# 表示容器大小为1020*600，启动时位于屏幕的（200,100)位置处（屏幕左上方顶点为原点）
root.geometry("1020x600+200+100")

# 添加Label元素，通常用于表示提示性文字
label_red = Label(root, text="红队(  )", font=('宋体',55), fg="#FF3300")
# place函数表示绝对定位，该元素位于容器原点（90，30）位置处
label_red.place(x=90, y=30)

label_red_score = Label(root, text="0", font=('宋体',70), fg="#FF3300")
label_red_score.place(x=290, y=25)

label_blue = Label(root, text="蓝队(  )", font=('宋体',55), fg="#3333FF")
label_blue.place(x=630, y=30)

label_blue_score = Label(root, text="0", font=('宋体',70), fg="#3333FF")
label_blue_score.place(x=830, y=25)

label_log = Label(root, text="两队得分记录", font=('宋体', 20), fg="green")
label_log.place(x=420, y=100)

# Entry表示文本框，用于记录两队的当局分数
entry_red = Entry(root, width=3, justify=CENTER, font=('宋体',80), fg="#FF3300")
entry_red.insert(0, "0")
entry_red.place(x=140, y=250)

entry_blue = Entry(root, width=3, justify=CENTER, font=('宋体',80), fg="#3333FF")
entry_blue.insert(0, "0")
entry_blue.place(x=720, y=250)

# Button为按钮，command参数绑定单击事件
button_end = Button(root, text=" 结束本局 ", width=9, font=('宋体',22), command=lambda: end_game())
button_end.place(x=150, y=500)

button_end = Button(root, text=" 开始本局 ", width=9, font=('宋体',25), bg="#33AA00", command=lambda: start_game())
button_end.place(x=425, y=500)

button_end = Button(root, text=" 撤消得分 ", width=9, font=('宋体',22), command=lambda: undo_score())
button_end.place(x=700, y=500)

button_red_plus = Button(root, text="+", width=3, font=('宋体',30), command=lambda: red_plus(1))
button_red_plus.place(x=190, y=150)

button_red_minus = Button(root, text="-", width=3, font=('宋体',30), command=lambda: red_minus(1))
button_red_minus.place(x=190, y=390)

button_blue_plus = Button(root, text="+", width=3, font=('宋体',30), command=lambda: blue_plus(1))
button_blue_plus.place(x=760, y=150)

button_blue_minus = Button(root, text="-", width=3, font=('宋体',30), command=lambda: blue_minus(1))
button_blue_minus.place(x=760, y=390)

# Text为文本域，用于记录得分日志
text_log = Text(root, height=14, width=24, font=('宋体',16))
text_log.place(x=380, y=160)

# 主线程正常启动UI界面
root.mainloop()