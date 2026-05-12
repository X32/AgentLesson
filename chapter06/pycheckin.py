import face_recognition, cv2, pyttsx3, time, numpy as np
from model import engine, Faces, Checks
from sqlmodel import Session, select, and_
from datetime import datetime, timedelta

# 从数据表faces中查找人脸编码，并构建一个[{},{}]数据保存所有userid与facecode
def get_encodings():
    with Session(engine) as session:
        faces = select(Faces).where(Faces.facecode!=None)
        results = session.execute(faces).mappings().all()
        user_encodings = []
        for result in results:
            facecode = result.Faces.facecode
            userid = result.Faces.userid
            # 构建字典对象，便于找到正确的userid以添加考勤记录
            user_encodings.append({"userid": userid, "facecode": eval(facecode)})
    return user_encodings

# 往数据表checks中插入考勤数据，如果同一个人在10分内考勤，将不记录
# 当天首次考勤将同时记录checkdate和checkstart，后续考勤无论多少次，只记录最后一次到checkend
def insert_checks(userid):
    with Session(engine) as session:
        # 先读取考勤表中当前用户当天是否有考勤记录（checkdate为空则表示没有)
        today = time.strftime("%Y-%m-%d")    # 获取当天日期
        nowtime = time.strftime("%H:%M:%S")  # 当前时间
        checks_date = select(Checks).where(and_(Checks.userid==userid, Checks.checkdate==today))
        result = session.execute(checks_date).first()
        if not result:   # 无当天考勤数据，则新增
            first_checks = Checks(userid=userid, checkdate=today, checkstart=nowtime)
            session.add(first_checks)
            session.commit()
            return "Checkin-OK"
        else:
            # 仅当时间间隔超过600秒时，才更新第二次考勤时间(调试时可修改得短一些时间）
            # 获取当前时间和打卡时间，并将其转换为datetime对象，以便于实现时间相减操作
            nowtime = datetime.strptime(nowtime, "%H:%M:%S")
            checkstart = datetime.strptime(str(result.Checks.checkstart), "%H:%M:%S")
            checkstatus = (nowtime - checkstart).seconds >= 600   # True或False

            # 如果已经有了第2次考勤数据，那么再次考勤的时间间隔也不能低于10分钟
            if result.Checks.checkend:
                checkend = datetime.strptime(str(result.Checks.checkend), "%H:%M:%S")
                checkstatus = checkstatus and (nowtime - checkend).seconds >= 600

            if checkstatus:
                result.Checks.checkend = nowtime   # 更新时间
                result.Checks.hours = round((nowtime-checkstart).seconds/3600, 1)
                session.commit()
                return "Checkin-OK"
            else:
                return "Checkin-Repeated"

        # 如果未进行考勤，则返回一个错误值
        return "Checkin-NOK"

# 比对人脸信息，并获取到匹配人脸对应的userid，用于新增考勤数据
def check_faces(image):
    # 先提取所有人脸的编码信息用于人脸比对
    user_encodings = get_encodings()
    coding_list = []
    for user_code in get_encodings():
        coding_list.append(np.array(user_code['facecode']))
    try:
        check_encoding = face_recognition.face_encodings(image, model='large')[0]
        match = face_recognition.compare_faces(coding_list, check_encoding, tolerance=0.5)
        if True in match:
            index = match.index(True)
            userid = user_encodings[index]['userid']
            insert_result = insert_checks(userid)   # 新增考勤数据
            return insert_result
    except:
        pass

    return "Checkin-NOK"

# 使用OpenCV打开摄像头并采集人脸，实时定位和渲染，并进行考勤
def check_camera():
    camera = cv2.VideoCapture(0)  # 为了方便测试，此处使用外置摄像头
    while True:
        ret, frame = camera.read()
        locations = face_recognition.face_locations(frame)
        if len(locations) >= 1:
            print(f"检测到{len(locations)}张人脸")
            top, right, bottom, left = locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), thickness=2)
            check_result = check_faces(frame)
            if "Checkin-OK" in check_result:
                pyttsx3.speak("考勤成功")
            elif "Checkin-Repeated" in check_result:
                pyttsx3.speak("请勿重复考勤")
            elif "Checkin-NOK" in check_result:
                pyttsx3.speak("考勤失败")

        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.5)

if __name__ == '__main__':
    check_camera()
    # insert_checks(3)