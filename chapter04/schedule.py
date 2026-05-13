import time
from crawler import get_hots, get_mils, get_news, get_tech_news
from summarize import get_and_update
from datetime import datetime


INTERVAL_SECONDS = 2 * 3600  # 执行间隔，默认2小时（7200秒）


def handle_on_time(now):
    get_hots()
    get_mils()
    get_news("blk_gnxw_011", "p_china")
    get_news("blk_gjxw_011", "p_world")
    get_news("blk_cjkjqcfc_011", "p_finance")
    get_news("blk_lctycp_011", "p_ent")
    get_news("blk_sh_011", "p_society")
    get_tech_news()
    get_and_update()
    print(f"更新新闻完成: {now}")


def run(interval_seconds=INTERVAL_SECONDS):
    while True:
        now = datetime.now()
        handle_on_time(now)
        print(f"下次执行时间: {(interval_seconds / 3600):.0f}小时后")
        time.sleep(interval_seconds)


if __name__ == '__main__':
    run()
   # now = datetime.now()
   # handle_on_time(now)