from fastapi import FastAPI, Request, Response
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key='Woniu123', session_cookie="SessionID")

# @app.middleware('http')
# async def set_session_id(request: Request, call_next):
#     response = await call_next(request)
#     SessionID = request.cookies.get('SessionID')
#     if SessionID:
#         response.set_cookie('SessionID', SessionID, httponly=True, max_age=15 * 24 * 60 * 60)
#     return response

# 设置Session变量userid和username
@app.get('/session/set')
def set_session(request: Request):
    session = request.session
    session['userid'] = 100
    session['username'] = 'woniu'
    return {"message": "成功设置Session变量"}

# 获取Session变量userid和username
@app.get('/session/get')
def get_session(request: Request):
    session = request.session
    userid = session.get('userid')
    username = session.get('username')
    return {"userid": userid, "username": username}

# Cookie变量的创建需要在Response对象中进行
@app.get('/cookie/set')
def set_cookie(response: Response):
    # 设置Cookie变量email，生命周期为10天，即使关闭浏览器也会保存在里面
    # 为了安全考虑防止XSS注入，建议设置httponly=True，表示只允许在协议中使用，无法使用JS代码读取
    response.set_cookie("email", "12345@qq.com", max_age=10*24*3600, httponly=True, )
    return {"message": "Cookie变量已设置"}

@app.get('/cookie/get')
def get_cookie(request: Request):
    # Cookie变量是保存在浏览器端的，所以变量值会以请求头Cookie发送给服务器
    email = request.cookies.get('email')
    return {"email": email}


if __name__ == '__main__':
    uvicorn.run(app)