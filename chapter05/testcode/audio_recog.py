# from modelscope import snapshot_download
#
# snapshot_download(model_id="iic/Whisper-large-v3-turbo", cache_dir="D:/AIModels")


# import os
# os.environ['KMP_DUPLICATE_LIB_OK']='True'

from transformers import pipeline
transcriber = pipeline(task="automatic-speech-recognition", model="openai/whisper-large-v3-turbo", device='cuda:0')      # 也支持参数 device_map="auto"， 但是该参数尽量不与 device 同时使用
result = transcriber("./test.wav")
# 也可以指定为一个URL地址对应的音频，如：
# result = transcriber("https://huggingface.co/datasets/Narsil/asr_dummy/resolve/main/mlk.flac")
print(result)   # 根据语音文件输出对应的文字



# import speech_recognition as sr
# import vosk, json, time
#
# r = sr.Recognizer()
# # r.vosk_model = vosk.Model(model_path="D:/AIModels/vosk-model-cn-0.22")
# r.vosk_model = vosk.Model(model_path="D:/AIModels/vosk-model-small-cn-0.22")
# audioFile = sr.AudioFile("test.wav")  # 不支持mp3，需要转换格式，此类情况不需要放在循环体中，一次性识别即可
# with audioFile as source:
#     audioData = r.record(source)
#     said = r.recognize_vosk(audioData)
#     print(json.loads(said)['text'])




# import speech_recognition as sr
# import vosk, json, time
#
# r = sr.Recognizer()
# r.vosk_model = vosk.Model(model_path="D:/AIModels/vosk-model-small-cn-0.22")
#
# while True:
#     mic = sr.Microphone()
#     with mic as source:
#         print("请说话...")
#         r.adjust_for_ambient_noise(source)
#         audioData = r.listen(source)
#
#     said = r.recognize_vosk(audioData)
#     print("你在说:", json.loads(said)['text'])



# from transformers import pipeline
# import speech_recognition as sr
#
# r = sr.Recognizer()
#
# transcriber = pipeline(task="automatic-speech-recognition", model="openai/whisper-large-v3-turbo", device='cpu')      # 也支持参数 device_map="auto"， 但是该参数尽量不与 device 同时使用
#
# while True:
#     mic = sr.Microphone()
#     with mic as source:
#         print("请说话...")
#         r.adjust_for_ambient_noise(source)
#         audioData = r.listen(source)
#
#     result = transcriber(audioData.get_wav_data())
#     print(result)