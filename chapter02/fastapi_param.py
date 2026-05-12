from fastapi import FastAPI
import uvicorn

app = FastAPI()

# 定义查询参数，即标准的URL地址，参数之间以 & 分隔
# 访问路径：http://127.0.0.1:8000/user/login?username=woniu&password=123456
@app.get("/user/login")
def user_login(username: str, password: str):
    if username == "woniu" and password == "123456":
        return {"message": "登录成功"}
    else:
        return {"message": "登录失败"}

# 定义路径参数，访问：http://127.0.0.1:8000/user/123，可获取user_id=123
@app.get("/user/{user_id}")
def get_user(user_id):
    return {"user_id": user_id}

# 也可以通过强制声明数据类型进而避免错误的参数传递
@app.get("/user2/{user_id}")
def get_user2(user_id: int):
    return {"user_id": user_id}



# # 定义一个Post请求的接口，模拟登录验证，并返回一个JSON
# @app.post("/user2/login")
# def login(username: str, password: str) -> dict:
#     if username == "woniu" and password == "123456":
#         return {"message": "登录成功"}
#     else:
#         return {"message": "登录失败"}

if __name__ == '__main__':
    uvicorn.run(app)