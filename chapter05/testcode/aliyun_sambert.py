# 将合成的语音保存到文件中（同步调用）

# import os, dashscope
# from dotenv import load_dotenv
# from dashscope.audio.tts import SpeechSynthesizer
#
# load_dotenv()
# dashscope.api_key = os.getenv('Dashscope_API_Key')
#
# result = SpeechSynthesizer.call(model='sambert-zhiqi-v1',  # 音色
#                                 text='今天天气怎么样，要不要外出游玩？',
#                                 sample_rate=48000,    # 频率
#                                 format='mp3')
# if result.get_audio_data() is not None:
#     with open('sambert.mp3', 'wb') as f:
#         f.write(result.get_audio_data())
# else:
#     print('出现错误', result.get_response())




import os, dashscope, pyaudio
from dotenv import load_dotenv
from dashscope.audio.tts import ResultCallback, SpeechSynthesizer, SpeechSynthesisResult

load_dotenv()
dashscope.api_key = os.getenv('Dashscope_API_Key')

class Callback(ResultCallback):
    _player = None
    _stream = None

    def on_open(self):
        print('Speech synthesizer is opened.')
        self._player = pyaudio.PyAudio()
        self._stream = self._player.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=48000,
            output=True)

    def on_event(self, result: SpeechSynthesisResult):
        if result.get_audio_frame() is not None:
            self._stream.write(result.get_audio_frame())

callback = Callback()
SpeechSynthesizer.call(model='sambert-zhichu-v1',
                       text='今天天气怎么样，要不要外出游玩？',
                       sample_rate=48000,
                       callback=callback)