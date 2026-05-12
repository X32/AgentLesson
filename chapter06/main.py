from fastapi import FastAPI, Request, Body, UploadFile, Form, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn, time, json, base64
from model import engine, Users, Faces, Checks
from sqlmodel import Session, select, desc
import face_recognition, cv2, numpy as np
from datetime import datetime
from livecheck import start_check

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/user')
def user(request: Request):
    with Session(engine) as session:
        # 左外连接时，由于在定义数据类时已经指定了外键关系，所以不需要使用On指定连接条件
        userfaces = select(Users, Faces.facecode).join(Faces, isouter=True).order_by(Users.userid)
        results = session.execute(userfaces).mappings().all()

    return templates.TemplateResponse(request=request, name="user.html", context={"results": results})

@app.post('/face/add')
def face_add(userid: int = Form(), file: UploadFile = File()):
    faceimage = file.file.read()
    # 直接将上传来的文件进行转码以适应face_recognition的类型需要
    image_array = np.frombuffer(faceimage, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    locations = face_recognition.face_locations(image)
    if len(locations) == 0:
        return "Face-Not-Exist"   # 响应给前端提示图片中没有人脸
    else:
        # 存在人脸数据情况下，则将人脸进行编码和保存
        encoding = face_recognition.face_encodings(image, model='large')[0]
        encoding = str(encoding.tolist())  # 转换为普通字符串用于保存

        with Session(engine) as session:
            faces = Faces(userid=userid, facecode=encoding)
            session.add(faces)
            session.commit()
            return "Face-Added"

@app.get('/check/month')
def check_month(request: Request):
    month_start = time.strftime("%Y-%m-01")
    with Session(engine) as session:
        user_check = select(Checks, Users).join(Users).where(Checks.checkdate>=month_start)
        results = session.execute(user_check).mappings().all()
    return templates.TemplateResponse(request=request, name="query.html", context={"results": results})

@app.get('/check/query/{filter}')
def check_query(request: Request, filter: str):
    filter = json.loads(filter)
    print(filter)
    username = filter['username']
    print(username)
    usersex = filter['usersex']
    department = filter['department']
    checkdate = filter['checkdate']

    with Session(engine) as session:
        user_check = select(Checks, Users).join(Users)
        if username:
            user_check = user_check.where(Users.username == username)
        if usersex:
            user_check = user_check.where(Users.usersex == usersex)
        if department:
            user_check = user_check.where(Users.department == department)
        if checkdate:
            user_check = user_check.where(Checks.checkdate == checkdate)
        results = session.execute(user_check).mappings().all()
    return templates.TemplateResponse(request=request, name="query.html", context={"results": results})

@app.get('/face/detect')
def detect(request: Request):
    return templates.TemplateResponse(request=request, name="detect.html")

@app.get('/')
def index(request: Request):
    with Session(engine) as session:
        today = datetime.now().date()
        today_check = select(Checks, Users).join(Users).where(Checks.checkdate == today).order_by(desc(Checks.checkend), desc(Checks.checkstart))
        results = session.execute(today_check).mappings().all()
    return templates.TemplateResponse(request=request, name="checkin.html", context={"results": results})

# 新建live.html模板页面并进行渲染
@app.get("/live")
def live(request: Request):
    return templates.TemplateResponse(request=request, name="live.html")

# 前端批量上传Base64编码的图片，后端解码并转换类型后进行检测
@app.post("/checkin/live")
def checkin_live(faces: list=Body()):
    live_images = []  # 保存包含有效人脸的图片
    for face in faces:
        # 将获取到的Base64编码进行解码，变成二进制，再进行类型转换变成可用图片
        image_data = base64.b64decode(face)
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # 判断该图片包含人脸，才作为活体检测的图片
        locations = face_recognition.face_locations(image)
        if len(locations) > 0:
            live_images.append(image)

    # 当有效人脸超过5张才视为有效，进入活体检测程序
    if len(live_images) >= 5:
        check_result = start_check(live_images)
        return check_result

    return "Checkin-NOK"


if __name__ == '__main__':
    uvicorn.run(app)