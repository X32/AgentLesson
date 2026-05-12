import os, signal, sys, dashscope, pyaudio
from dashscope.audio.asr import *
from dotenv import load_dotenv
load_dotenv()

mic = None
stream = None
dashscope.api_key = os.getenv('Dashscope_API_Key')

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

    # def on_close(self) -> None:
    #     global mic
    #     global stream
    #     print('RecognitionCallback close.')
    #     stream.stop_stream()
    #     stream.close()
    #     mic.terminate()
    #     stream = None
    #     mic = None

    # def on_complete(self) -> None:
    #     print('语音识别完成.')  # recognition completed

    # def on_error(self, message) -> None:
    #     print('语音识别出错: ', message.message)
    #     # Stop and close the audio stream if it is running
    #     if 'stream' in globals() and stream.active:
    #         stream.stop()
    #         stream.close()
    #     # Forcefully exit the program
    #     sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()

        # 中途识别结果
        # if 'text' in sentence:
        #     print('识别结果为: ', sentence['text'])

        # 一句话结束后的识别结果
        if RecognitionResult.is_sentence_end(sentence):
            print('识别结果为: ', sentence['text'])


# main function
if __name__ == '__main__':
    callback = Callback()

    recognition = Recognition(
        model='paraformer-realtime-v2',
        format='pcm',  # 支持 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr'
        sample_rate=16000,
        semantic_punctuation_enabled=False,
        callback=callback)

    recognition.start()

    while True:
        if stream:
            data = stream.read(3200, exception_on_overflow=False)
            recognition.send_audio_frame(data)
        else:
            break

    recognition.stop()