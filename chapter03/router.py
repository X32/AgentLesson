from fastapi import APIRouter, Form

# 模块名称为：mytest，用该对象来定义接口
mytest = APIRouter()

# 定义接口
@mytest.get('/get_test')
def get_test():
    return 'Test Get'

@mytest.post('/post_test')
def post_test(data: str=Form()):
    return 'Test Post'