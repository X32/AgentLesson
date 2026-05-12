from http import HTTPStatus
import os, dashscope
from dotenv import load_dotenv
load_dotenv()

try:
    dashscope.api_key = os.getenv('Dashscope_API_Key')
    recognition = dashscope.audio.asr.Recognition(model='paraformer-realtime-v2',
                          format='wav',
                          sample_rate=16000,
                          language_hints=['zh', 'en'],
                          callback=None)

    result = recognition.call(r'C:\Users\Denny\Downloads\8986223657.wav')
    if result.status_code == HTTPStatus.OK:
        content = ""
        sentences = result.get_sentence()
        for sentence in sentences:
            content += sentence['text']
        print('识别结果：', content)
    else:
        print('出现错误: ', result.message)
except:
    pass






# import json, os
# from dotenv import load_dotenv
# from urllib import request
# from http import HTTPStatus
# import dashscope
#
# load_dotenv()
#
# # 支持同时识别多个音频文件，但是必须先确保该音频文件拥有公网URL地址，否则云平台无法正常访问到
# task_response = dashscope.audio.asr.Transcription.async_call(
#     model='paraformer-v2',
#     api_key=os.getenv('Dashscope_API_Key'),
#     file_urls=[
#         'https://woniumd.oss-cn-hangzhou.aliyuncs.com/ai/dengqiang/test.wav',
#         'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav'
#     ],
#     language_hints=['zh', 'en'])
#
# transcription_response = dashscope.audio.asr.Transcription.wait(
#     task=task_response.output.task_id)
#
# if transcription_response.status_code == HTTPStatus.OK:
#     for transcription in transcription_response.output['results']:
#         url = transcription['transcription_url']
#         result = json.loads(request.urlopen(url).read().decode('utf8'))
#         print("识别结果：", result['transcripts'][0]['text'])
#     print('录音文件识别完成。')
# else:
#     print('出错了: ', transcription_response.output.message)