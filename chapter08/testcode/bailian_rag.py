import os, dashscope
from openai import OpenAI
from alibabacloud_bailian20231229.client import Client as BailianClient
from alibabacloud_bailian20231229 import models as BailianModels
from alibabacloud_credentials.client import Client as CredClient
from alibabacloud_credentials.models import Config as CredConfig
from alibabacloud_tea_openapi.models import Config as OpenAPIConfig

from dotenv import load_dotenv
load_dotenv()

Bailian_WorkspaceId = os.getenv("Bailian_WorkspaceId")
Bailian_CategoryId = os.getenv("Bailian_CategoryId")
Bailian_Access_Key_ID = os.getenv("Bailian_Access_Key_ID")
Bailian_Access_Key_Secret = os.getenv("Bailian_Access_Key_Secret")

def create_client():
    cred_config  = CredConfig(
        type='access_key',
        access_key_id=Bailian_Access_Key_ID,
        access_key_secret=Bailian_Access_Key_Secret,
    )
    credential = CredClient(cred_config)
    # print(credential.get_credential().get_access_key_secret())
    bailian_config = OpenAPIConfig(credential=credential)
    bailian_config.endpoint = "bailian.cn-beijing.aliyuncs.com"
    bailian_client = BailianClient(config=bailian_config)
    return bailian_client

def list_file():
    client = create_client()
    list_file_request = BailianModels.ListFileRequest(category_id=Bailian_CategoryId)
    result = client.list_file(workspace_id=Bailian_WorkspaceId, request=list_file_request)
    print(result)

def create_index():
    # 不可用，无法添加文档
    client = create_client()
    create_index_request = BailianModels.CreateIndexRequest(
        document_ids=['file_0610e3632b56476fbf43302703942c10_10034389',
                      'file_a3691b1bb9f14563bdd67afb4fc6401f_10034389'],
        name="MyIndex-2",
        structure_type = "unstructured",
        sink_type = "BUILT_IN")
    result = client.create_index(workspace_id=Bailian_WorkspaceId, request=create_index_request)
    print(result)

def query_index(query_string):
    client = create_client()
    retrieve_request = BailianModels.RetrieveRequest(index_id='hkdtb1ie4j', query=query_string)
    result = client.retrieve(workspace_id=Bailian_WorkspaceId, request=retrieve_request)
    print(len(result.body.data.nodes))
    return result.body.data


def chat_llm(message):
    rag = str(query_index(message))
    print(rag)
    client = OpenAI(
        api_key=os.getenv("Dashscope_API_Key"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': f'请基于以下内容\n{rag}]\n，回答用户的问题：\n{message}'}],
        stream=True,
        stream_options={"include_usage": True}
    )

    for chunk in completion:
        if len(chunk.choices) > 0:
            print(chunk.choices[0].delta.content, end="")

if __name__ == '__main__':
    result = query_index("任正非创建华为的背景是什么？")
    print(result)
    # chat_llm("任正非创建华为的背景是什么？")