# 导入face_recognition和opencv
import face_recognition, cv2

# 加载图片
image = face_recognition.load_image_file("../faces/conference-room.jpeg")

# 获取图片中的人脸位置
locations = face_recognition.face_locations(image)

# 遍历所有人脸位置数据
for location in locations:
    top, right, bottom, left = location
    # face_image = image[top:bottom, left:right]
    # 在图片中绘制矩形方框，将人脸标识出来
    # 只需要提供坐标位置和框线的颜色及宽度
    cv2.rectangle(image, (left, top), (right, bottom), (0,0,255), thickness=2)
# 使用OpenCV将图片显示出来
cv2.imshow("Face", image)
cv2.waitKey(0)

# 也可以使用OpenCV将该图片进行保存
cv2.imwrite("../faces/conference-room-2.jpeg", image)