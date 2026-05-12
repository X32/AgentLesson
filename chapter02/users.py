from sqlmodel import create_engine

# 连接到woniuai数据库
engine = create_engine("mysql+pymysql://qiang:123456@127.0.0.1:3306/woniuai")

# 定义数据表的映射关系
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Users(SQLModel, table=True):
    userid: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    phone: str
    role: str
    createtime: datetime

    __tablename__ = "users"

# 创建users表，由于已经创建此步操作可以不做
# SQLModel.metadata.create_all(engine)