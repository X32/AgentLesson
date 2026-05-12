import os, requests
from dotenv import load_dotenv
load_dotenv()

def aliyun_search(content):
    print(content)
    url = "http://default-w4yy.platform-cn-shanghai.opensearch.aliyuncs.com/v3/openapi/workspaces/default/web-search/ops-web-search-001"
    header = {"Content-Type": "application/json", "Authorization": f"Bearer {os.getenv('Aliyun_Search_Key')}"}
    # way=full：使用大模型对搜索结果进行评判和过滤，默认为：fast，不过滤
    # content_type=summary：对网页内容的文本进行摘要，默认为：snippet，简短描述
    data = {"query": content, "top_k":3, "way":"full", "content_type":"summary"}
    resp = requests.post(url, headers=header, json=data)

    list = resp.json()['result']['search_result']
    return list


messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": "data:image/png;base64,{图像的base64编码}"
                },
            },
            {"type": "text", "text": "图中描绘的是什么景象?"},
        ],
    },
]
