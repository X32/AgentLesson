from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
# 实现化Jinja2模板引擎，并设定模板文件的目录为：templates
templates = Jinja2Templates(directory="templates")

# 添加自定义函数到Jinja2中，可在模板页面调用
def get_user():
    return {"username":"woniu", "password":"123456"}
templates.env.globals.update(get_user=get_user)

# 设定响应的类型为HTMLResponse，以使用text/html来作为响应类型
# 在函数中必须要定义Request作为参数，这是固定要求
@app.get('/jinja2', response_class=HTMLResponse)
def jinja2_output(request: Request):
    article = {"author": "蜗牛学苑",
               "title": "如何使用Jinja2",
               "count": 120}
    # 将字典对象article作为模板变量对basic.html中的变量进行填充
    return templates.TemplateResponse(request=request, name="basic.html", context=article)

@app.get('/core', response_class=HTMLResponse)
def jinja2_core(request: Request):
    return templates.TemplateResponse(request=request, name="core.html", context={"count":100})

@app.get('/book', response_class=HTMLResponse)
def jinja2_book(request: Request):
    books = [
        {'id': 1, 'title': 'PHP教程', 'author': '张三', 'price': 52},
        {'id': 2, 'title': 'Python教程', 'author': '李四', 'price': 36},
        {'id': 3, 'title': 'Java教程', 'author': '王五', 'price': 68}
    ]
    return templates.TemplateResponse(request=request, name="book.html", context={"books":books})

if __name__ == '__main__':
    uvicorn.run(app)