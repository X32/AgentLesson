import pyttsx3

engine = pyttsx3.init()    # 初始化tts引擎
engine.setProperty('volume', 1.0)   # 设置音量（0到1之间）
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)   # 设置语速
# 要播报的文本
text = "本地语音合成接口合成效率高速度快，但是可选择的音色单一，体验欠佳"
# 直接播报语音
pyttsx3.speak(text)
# 或将合成的语音保存到文件中
# engine.save_to_file(text=text, filename="./pyttsx3.wav")
# engine.runAndWait()
