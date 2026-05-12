from users import Users, engine
from sqlmodel import Session, text, select, and_, func,desc

# 执行原生SQL语句
sql = text("select * from users where userid=:userid")
with Session(engine) as session:
    result = session.execute(sql, {"userid": 1})
# 如果要获取列名，则需要使用mappings方法
print(result.mappings().fetchone())

# 执行多条件where语句
with Session(engine) as session:
    user = select(Users).where(and_(Users.userid == 2, Users.username == 'woniu'))
    print(session.execute(user).all())

# 也可以通过该方式进行查询，并且只查询userid和username两列
with Session(engine) as session:
    user = select(Users.userid, Users.username).filter(and_(Users.userid == 2, Users.username == 'woniu'))
    print(session.execute(user).mappings().all())

# 执行group by分组查询，并统计每个角色的数量
with Session(engine) as session:
    user = select(Users.role, func.count(Users.userid)).group_by(Users.role)
    print(session.execute(user).all())

# 倒序排列
with Session(engine) as session:
    user = select(Users).order_by(desc(Users.userid))
    print(session.execute(user).all())