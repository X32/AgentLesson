# 对请求参数进行验证

from fastapi import FastAPI, Form, Query
import uvicorn

app = FastAPI()

# 路径参数{name}无默认值，查询参数age必须为整数且默认值为20
@app.get("/user/{name}")
def get_user(name: str|None, age: int=Query(default=20)):
    return {name, age}

# 查询参数页number默认值为1，且必须介于1~20之间的值
# ge：greater than or eqaul，表示大于等于，le表示小于等于
# 与之对应的还有：gt：大于，lt: 小于
@app.get('/page/')
def list_page(number: int = Query(default=1, ge=1, le=20)):
    return {"page": number}

# 表单数据username必须介于5~20之间的长度，password介于6~18的长度
# phone必须是一个有效的中国移动电话号码，支持正则验证
@app.post("/login")
def login(username: str=Form(default="woniu", min_length=5, max_length=20),
          password: str=Form(default="123456", min_length=6, max_length=18),
          phone: str=Form(pattern="^1[3-9]\\d{9}$")):
    return {"username": username, "password": password, "phone": phone}

if __name__ == '__main__':
    uvicorn.run(app)