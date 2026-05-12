from fastapi import FastAPI, Body
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# 直接获取整个Post请求体，并设置请求类型为JSON
@app.post('/json')
def read_json(user: dict=Body()):
    # 对获取到的JSON对象简单输出到响应中
    return {user["username"]: user["password"]}

# 定义数据模型用于映射JSON数据格式
class Item(BaseModel):
    username: str
    password: str
    salary: float
    address: str|None=None   # 表示参数可选，默认值为空

# 通过Post请求读取请求正文数据并获取到字段的值
@app.get('/items/{item_id}')
def get_item_by_id(item_id: str):
    try:
        return {"item_id": int(item_id)}
    except ValueError:
        return {"error": "Invalid ID type"}


@app.post('/item')
def get_item(item: Item):
    username = item.username
    password = item.password
    salary = item.salary
    address = item.address
    if username == "woniu" and password == "123456":
        return {"message": "登录成功"}
    else:
        return {"message": "登录失败"}


if __name__ == '__main__':
    uvicorn.run(app)