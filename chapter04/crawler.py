import requests
from bs4 import BeautifulSoup
from sqlmodel import Session, select
from datetime import datetime
from news import engine, News

url = "https://news.sina.com.cn/"
resp = requests.get(url)
resp.encoding = 'utf-8'
html = BeautifulSoup(resp.text, 'lxml')

# 获取今日要闻的标题与超链接
def get_hots():
    daily_hots = html.find(name="div", id="syncad_1", class_="ct_t_01")
    for hots in daily_hots.find_all("h1", attrs={"data-client": "headline"}):
        links = hots.find_all("a", class_="linkNewsTopBold")
        for link in links:
            hyperlink = link.get("href")
            headline = link.text
            category = "hot"
            news = News(category=category, headline=headline, hyperlink=hyperlink, createtime=datetime.now())
            insert_news(news)

# 获取军事新闻标题与超链接
def get_mils():
    mil_news = html.find(name="div", id="blk_08_cont01", attrs={"data-sudaclick":"mil_1"})
    for line in mil_news.find_all("li"):
        link = line.find("a")
        hyperlink = link.get("href")
        headline = link.text
        category = "mil"
        news = News(category=category, headline=headline, hyperlink=hyperlink, createtime=datetime.now())
        insert_news(news)

# 获取国内国际科技娱乐军事等类别新闻
def get_news(id, type):
    daily_news = html.find(name="ul", id=id, class_="list_14_noBg", attrs={"data-client": type})
    for line in daily_news.find_all("li"):
        link = line.find("a")
        hyperlink = link.get("href")
        headline = link.text
        category = type[2:]
        news = News(category=category, headline=headline, hyperlink=hyperlink, createtime=datetime.now())
        insert_news(news)

# 新增数据到数据库中
def insert_news(news):
    with Session(engine) as session:
        hyperlink = news.hyperlink
        query = select(News.id).where(News.hyperlink == hyperlink)
        result = session.exec(query).all()
        if len(result) > 0:
            print(f"数据{result}已经存在，不需要更新")
        else:
            session.add(news)
            session.commit()

if __name__ == '__main__':
    # get_hots()
    get_mils()
    # get_news("blk_gnxw_011", "p_china")
    # get_news("blk_gjxw_011","p_world")
    # get_news("blk_cjkjqcfc_011", "p_finance")
    # get_news("blk_lctycp_011", "p_ent")
