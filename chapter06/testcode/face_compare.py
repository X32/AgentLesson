import face_recognition, cv2, time

# 加载多人照片
image_all = face_recognition.load_image_file("../faces/conference-room.jpeg")

# 加载单人照片（本照片由AI进行二次创作，特征有所区别）
image_zhang = face_recognition.load_image_file("../faces/Mr-Zhang.png")

# 对两张照片进行人脸编码，每一张人脸均有独立编码
all_encodings = face_recognition.face_encodings(image_all, model='large')
zhang_encoding = face_recognition.face_encodings(image_zhang, model='large')[0]

# 将单张人脸与多张人脸的图片编码进行匹配，tolerance越小，说明匹配要求越严格
# 本书所使用的tolerance参数并无实际指导价值，读者需要根据实际情况进行调整
match = face_recognition.compare_faces(all_encodings, zhang_encoding, tolerance=0.4)
index = match.index(True)   # 找到匹配的人脸的下标

# 找到多人图片的全部人脸的位置数据，并获取比对成功的人脸的位置
locations = face_recognition.face_locations(image_all)
top, right, bottom, left = locations[index]
cv2.rectangle(image_all, (left, top), (right, bottom), (0,0,255), thickness=2)
# 利用OpenCV绘制文字在图上标注一些文字说明，如姓名或称呼等
cv2.putText(image_all, "Mr-Zhang", (left-5, bottom+30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), thickness=2)
# 保存带文字标注的图片到文件中，也可以使用cv2.imshow实时显示
cv2.imwrite("../faces/face-compare.jpg", image_all)