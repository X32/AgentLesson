from fastapi import FastAPI, Form
import uvicorn
from users import Users, engine
from sqlmodel import Field, Session, SQLModel

app = FastAPI()

# 查询所有用户数据，返回JSON
@app.get("/users")
def get_users():
    with Session(engine) as session:
        users = session.query(Users).all()
        return users

# 查询单个用户数据，JSON返回
@app.get("/users/{user_id}")
def get_user(user_id):
    with Session(engine) as session:
        user = session.query(Users).filter_by(userid=user_id).first()
        return user

# 新增一个用户，并返回用户id
@app.post("/users")
def create_user(user: Users):
    username = user.username  # 先获取用户名用户查询新增用户的userid
    with Session(engine) as session:
        session.add(user)   # 执行insert语句新增用户
        session.commit()    # 提交新增数据到数据库中
        # 查询用户id
        new = session.query(Users).filter_by(username=username).first()
    return new.userid

# 修改某用户的电话号码
@app.put("/users/{user_id}")
def update_user(user_id, phone: str=Form()):
    with Session(engine) as session:
        # 先通过用户id获取到用户表
        user = session.query(Users).filter_by(userid=user_id).first()
        userid = user.userid   # 获取userid用于返回
        user.phone = phone     # 修改用户的电话号码
        session.commit()
    return userid

# 删除一个用户，并返回用户id
@app.delete("/users/{user_id}")
def delete_user(user_id):
    with Session(engine) as session:
        # 先通过用户id获取到用户表
        user = session.query(Users).filter_by(userid=user_id).first()
        userid = user.userid
        session.delete(user)
        session.commit()
    return userid

if __name__ == '__main__':
    uvicorn.run(app)