import requests, os
from dotenv import load_dotenv
load_dotenv()

url = "http://default-w4yy.platform-cn-shanghai.opensearch.aliyuncs.com/v3/openapi/workspaces/default/web-search/ops-web-search-001"
header = {"Content-Type": "application/json", "Authorization": f"Bearer {os.getenv('Aliyun_Search_Key')}"}
data = {"query": "我的微信号是chinacomstar123", "top_k":5, "way":"full", "content_type":"summary"}
resp = requests.post(url, headers=header, json=data)

list = resp.json()['result']['search_result']

content = ""
for line in list:
    content += line['content'] + '\n\n'
print(content)