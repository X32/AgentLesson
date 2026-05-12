from sqlmodel import create_engine

# 连接到woniuai数据库
engine = create_engine("mysql+pymysql://qiang:123456@127.0.0.1:3306/checkin")

# 定义数据表的映射关系
from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime, date, time

class Users(SQLModel, table=True):
    # 定义主键及其他列
    userid: Optional[int] = Field(default=None, primary_key=True)
    username: str
    usersex: str
    department: str
    createtime: datetime

class Faces(SQLModel, table=True):
    # 定义了主键和外键，进行多表查询时会自动生成主外键关联的过滤条件
    faceid: Optional[int] = Field(default=None, primary_key=True)
    userid: int | None = Field(default=None, foreign_key="users.userid")
    facecode: str

class Checks(SQLModel, table=True):
    checkid: Optional[int] = Field(default=None, primary_key=True)
    userid: int | None = Field(default=None, foreign_key="users.userid")
    checkdate: date
    checkstart: time
    checkend: time
    hours: float