import face_recognition, cv2, time

# 获取摄像头#0(默认为笔记本内置摄像头)
camera = cv2.VideoCapture(0)

# 循环读取视频帧并进行实时渲染
while True:
    # 读取到视频帧frame
    ret, frame = camera.read()
    # 进行人脸识别和标注
    locations = face_recognition.face_locations(frame)
    if len(locations) > 0:
        print(f"检测到{len(locations)}张人脸")
        # 标注出现在视频中的每一张人脸
        for location in locations:
            top, right, bottom, left = location
            # face_image = frame[top:bottom, left:right]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), thickness=2)
    else:
        print("未检测到人脸")

    # 实时渲染摄像头数据，按q键退出
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.1)   # 间隔100毫秒渲染一次，也可以更快

camera.release()      # 释放摄像头实例