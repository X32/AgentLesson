# 每日新闻摘要系统

## 项目架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                        定时调度层 (schedule.py)                       │
│              每2小时触发一次爬取 + 摘要的完整流程                        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │                     │
          ┌─────────▼─────────┐  ┌───────▼───────────┐
          │   crawler.py      │  │  summarize.py     │
          │   (数据采集层)      │  │  (AI摘要层)        │
          │                   │  │                    │
          │  news.sina.com.cn │  │  1.按超链接爬取正文  │
          │  ├─ get_hots()    │  │  2.调用LLM生成摘要  │
          │  ├─ get_mils()    │  │  3.更新summary字段  │
          │  └─ get_news()    │  │                    │
          │                   │  │  .env 配置:         │
          │  tech.sina.com.cn │  │  ├─ LLM_API_KEY    │
          │  ├─ get_tech_     │  │  ├─ LLM_BASE_URL   │
          │  │  headlines()   │  │  └─ LLM_MODEL      │
          │  └─ get_tech_     │  │                    │
          │     feed()        │  │  支持: Qwen/DeepSeek│
          └────────┬──────────┘  └────────┬───────────┘
                   │                      │
                   │  写入                 │  读取 + 更新
                   ▼                      ▼
          ┌─────────────────────────────────────────┐
          │            MySQL (dailynews)             │
          │            news.py (ORM层)               │
          │                                         │
          │  News 表:                                │
          │  ┌──────────┬──────────┬──────────────┐  │
          │  │ id       │ headline │ hyperlink    │  │
          │  │ category │ content  │ summary      │  │
          │  │ createtime          │              │  │
          │  └──────────┴──────────┴──────────────┘  │
          │                                         │
          │  .env 配置:                               │
          │  ├─ DB_HOST / DB_PORT                    │
          │  ├─ DB_NAME / DB_USER                    │
          │  └─ DB_PASSWORD                          │
          └──────────────────┬──────────────────────┘
                             │
                             │ SQLModel 查询
                             ▼
          ┌─────────────────────────────────────────┐
          │        main.py (Web后端 / FastAPI)       │
          │                                         │
          │  路由:                                   │
          │  ├─ GET /              → 今日要闻        │
          │  ├─ GET /{category}    → 按分类查询      │
          │  └─ GET /{date}/{cat}  → 按日期+分类查询 │
          │                                         │
          │  分类: hot china world mil finance        │
          │        tech ent society                  │
          └──────────────────┬──────────────────────┘
                             │
                             │ Jinja2 渲染
                             ▼
          ┌─────────────────────────────────────────┐
          │     templates/news.html (前端展示层)      │
          │                                         │
          │  ┌───────────────────────────────────┐   │
          │  │  导航栏: 日期 + 8个分类链接          │   │
          │  ├───────────────────────────────────┤   │
          │  │  新闻列表 (循环渲染)                │   │
          │  │  ├─ 标题 + 查看原文链接             │   │
          │  │  └─ AI摘要内容                     │   │
          │  ├───────────────────────────────────┤   │
          │  │  底部: 历史日期导航                  │   │
          │  └───────────────────────────────────┘   │
          └─────────────────────────────────────────┘
```

## 数据流向

```
新浪新闻网页 → crawler.py(爬取) → MySQL(存储) → summarize.py(LLM摘要) → main.py(FastAPI路由) → news.html(浏览器展示)
```

## 各层职责

| 层级   | 文件                    | 职责                                                                    |
| ------ | ----------------------- | ----------------------------------------------------------------------- |
| 调度层 | `schedule.py`         | 定时触发爬取和摘要，每2小时运行一次                                     |
| 采集层 | `crawler.py`          | 爬取 `news.sina.com.cn`(7个分类) + `tech.sina.com.cn`(科技)，写入DB |
| AI层   | `summarize.py`        | 爬取新闻正文，调用LLM生成100字摘要，更新DB                              |
| ORM层  | `news.py`             | SQLModel模型定义 + DB连接 + 查询方法                                    |
| 后端层 | `main.py`             | FastAPI路由，按日期/分类查询，Jinja2渲染模板                            |
| 前端层 | `templates/news.html` | 展示新闻列表、分类导航、历史日期                                        |
| 配置层 | `.env`                | 数据库配置 + LLM模型配置(支持Qwen/DeepSeek切换)                         |

## 执行顺序

1. `python crawler.py` — 爬取新闻标题和链接，写入数据库（summary 字段为空）
2. `python summarize.py` — 读取未生成摘要的新闻，调用 LLM API 生成摘要并更新数据库
3. `python main.py` — 启动 FastAPI Web 服务，查询已摘要的新闻并展示

`schedule.py` 是把步骤1和2合并定时执行的：

```
schedule.py
  └── 每 2 小时触发：
      ├── crawler.py  (爬取)
      └── summarize.py (摘要)
```

## LLM 模型配置

在 `.env` 中配置 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL` 三个项，切换模型只需修改配置：

| 模型     | LLM_BASE_URL                                          | LLM_MODEL         |
| -------- | ----------------------------------------------------- | ----------------- |
| DeepSeek | `https://api.deepseek.com`                          | `deepseek-chat` |
| Qwen     | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus`     |

## 依赖

fastapi, uvicorn, sqlmodel, pymysql, beautifulsoup4, lxml, openai, python-dotenv, requests, jinja2



# 1. 启动 Web 服务（主入口）

  python main.py

# 2. 手动运行爬虫抓取新闻

  python crawler.py

# 3. 对今天未摘要的新闻生成摘要

  python summarize.py

# 4. 启动定时任务（每2小时的30分自动爬虫+摘要）

  python schedule.py


# 查看容器运行状态

  docker compose ps

# 查看应用日志

  docker compose logs app

# 实时查看应用日志

  docker compose logs -f app

# 查看 MySQL 日志

  docker compose logs mysql

# 查看应用容器内的环境变量

  docker compose exec app env

# 进入应用容器内部

  docker compose exec app bash

# 进入 MySQL 容器

  docker compose exec mysql bash

# 测试 Web 服务是否正常

  curl http://localhost:8000



Docker Compose 已经用命名卷持久化了数据：

  volumes:
    - mysql_data:/var/lib/mysql    # 数据存在命名卷中，不受容器影响

  容器删除不影响数据 — docker compose down 只删除容器，命名卷 chapter04_mysql_data
  仍然保留，下次 up 数据还在。

  只有在以下情况数据会丢失：

- docker compose down -v（-v 会同时删除命名卷）
- 手动删除卷：docker volume rm chapter04_mysql_data

  如果要备份数据：

# 备份到本地文件

  docker compose exec mysql mysqldump -uroot -pX12345678x dailynews > backup.sql

# 恢复

  docker compose exec -T mysql mysql -uroot -pX12345678x dailynews < backup.sql

  如果要重置（清空所有数据）：
  docker compose down -v    # 删除容器和数据卷
  docker compose up -d      # 重新初始化

  所以不用担心，正常的 down 和 up 不会丢失数据，-v 才会。


docker compose down -v && docker compose up -d --build

docker compose down -v 

docker compose up -d

docker compose up -d --build



修改了应用代码（.py 文件或 templates），需要重新构建镜像并重启 app
  容器，数据库数据保持不变。

  docker compose up -d --build app

  原理：

- --build — 重新根据 Dockerfile 构建 app 镜像（新代码打包进去）
- app — 只重建 app 服务，不影响 MySQL 容器和数据卷
- -d — 后台运行

  MySQL 容器和数据卷不受影响，数据完好保留。

✻ Brewed for 11s

❯ 如果修改了数据库怎么办

● 修改了 dailynews.sql 后，MySQL 不会自动重新执行，因为数据卷已经存在了。

  重新初始化数据库（数据会丢失）：
  docker compose down -v && docker compose up -d
  -v 删除数据卷，下次启动时 MySQL 检测到空卷，会重新执行初始化脚本。

  如果只想加表/加字段，不想丢数据：

# 直接在运行中的 MySQL 里执行 SQL

  docker compose exec mysql mysql -uroot -pX12345678x dailynews

# 进入后手动执行 ALTER/CREATE 语句，或

# 把改好的 SQL 通过管道输入

  docker compose exec -T mysql mysql -uroot -pX12345678x dailynews < dailynews.sql

  总结：docker compose down -v 适合开发阶段测试用，生产环境应该用 ALTER TABLE
  等增量变更，避免丢数据。

✻ Cooked for 6s

❯ 如果修改了配置文件或模板文件呢

● 取决于你改了什么文件，分为三种情况：

  模板文件（templates/） — 已编译进镜像，需要重建：
  docker compose up -d --build app

  .env 配置文件 — 注入到容器环境变量中，不需要重建，只需重启：
  docker compose restart app

  docker-compose.yml / Dockerfile — 结构发生变化，需要重建：
  docker compose up -d --build


  总结：

  修改的文件: .py / templates/
  命令: docker compose up -d --build app
  数据: 保留
  ────────────────────────────────────────
  修改的文件: .env
  命令: docker compose restart app
  数据: 保留
  ────────────────────────────────────────
  修改的文件: docker-compose.yml / Dockerfile
  命令: docker compose up -d --build
  数据: 保留
  ────────────────────────────────────────
  修改的文件: dailynews.sql
  命令: docker compose down -v && docker compose up -d
  数据: 丢失
