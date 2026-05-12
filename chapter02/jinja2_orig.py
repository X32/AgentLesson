from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get('/html')
def html_output():
    username = "woniu"
    html = '''
        <div style="width: 300px; height: 200px; margin:auto; border: solid 2px red;">
            <a href="#">蜗牛学苑</a>
            <ul>
                <li>这是菜单项一</li>
                <li>这是菜单项二</li>
                <li>这是菜单项三</li>
                <li>这是菜单项四</li>
            </ul>
            <p>欢迎 %s 登录.</p>
        </div>
        ''' % username

    return HTMLResponse(html)


if __name__ == '__main__':
    uvicorn.run(app)