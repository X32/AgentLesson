import face_recognition, cv2, numpy as np

image = face_recognition.load_image_file("../faces/face-68.png")
landmarks = face_recognition.face_landmarks(image)
# print(landmarks)

# 绘制眼睛轮廓线条
# print(landmarks[0]['left_eye'])
# print(landmarks[0]['right_eye'])
cv2.polylines(image, [np.array(landmarks[0]['left_eye'], np.int32)], True, (0, 255, 0), 2)
cv2.polylines(image, [np.array(landmarks[0]['right_eye'], np.int32)], True, (0, 255, 0), 2)

# 绘制嘴巴轮廓线条
cv2.polylines(image, [np.array(landmarks[0]['top_lip'], np.int32)], True, (0, 255, 0), 2)
cv2.polylines(image, [np.array(landmarks[0]['bottom_lip'], np.int32)], True, (0, 255, 0), 2)

cv2.imshow("Face", image)
cv2.waitKey(0)