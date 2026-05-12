import time
from sqlmodel import Field, SQLModel, Session, select, between
from typing import Optional
from datetime import datetime
from sqlmodel import create_engine

engine = create_engine("mysql+pymysql://qiang:123456@127.0.0.1:3306/dailynews")

#　创建SQLModel关系映射类
class News(SQLModel, table=True,):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str
    headline: str
    hyperlink: str
    content: str
    summary: str
    createtime: datetime

def get_news_by_dc(date=None, category='hot'):
    if date is None:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
        endtime = time.strftime("%Y-%m-%d 23:59:59")
    else:
        starttime = time.strftime(f"{date} 00:00:00")
        endtime = time.strftime(f"{date} 23:59:59")

    with Session(engine) as session:
        sql = select(News).where(News.category==category).where(between(News.createtime, starttime, endtime)).where(News.summary!="")
        news = session.execute(sql).mappings().all()
        return news

if __name__ == '__main__':
    get_news_by_date(date='2025-02-28')