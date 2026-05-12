import face_recognition, numpy as np
from pycheckin import check_faces

# 将前端连续截图的图片作为参数传递进来
def start_check(live_images):
    numbers = []   # 保存每次检测到的值
    for image in live_images:
        landmarks = face_recognition.face_landmarks(image)
        ear = calc_ear(landmarks)
        numbers.append(ear)

    # 计算连续N个EAR数据的标准差并判断是否为活体
    ear_ratio = np.std(numbers)/np.average(numbers)
    print(ear_ratio)
    if ear_ratio > 0.2:
        # 找到一张相对正常的照片用于考勤
        index = numbers.index(max(numbers))
        check_result = check_faces(live_images[index])
        return check_result
    else:
        return "Checkin-Not-Live"

def calc_ear(landmarks):
    left_eye = np.array(landmarks[0]['left_eye'])
    right_eye = np.array(landmarks[0]['right_eye'])

    left_1_4 = np.linalg.norm(left_eye[0] - left_eye[3])
    left_2_6 = np.linalg.norm(left_eye[1] - left_eye[5])
    left_3_5 = np.linalg.norm(left_eye[2] - left_eye[4])
    left_ear = (left_2_6 + left_3_5) / (left_1_4 * 2)

    right_1_4 = np.linalg.norm(right_eye[0] - right_eye[3])
    right_2_6 = np.linalg.norm(right_eye[1] - right_eye[5])
    right_3_5 = np.linalg.norm(right_eye[2] - right_eye[4])
    right_ear = (right_2_6 + right_3_5) / (right_1_4 * 2)

    return (left_ear + right_ear) / 2


def calc_nod(landmarks):
    pass


def calc_mar(landmarks):
    pass


# 改进一下提示信息，否则只有成功与失败，不合适，加重复考勤，动作不匹配等
# 眨眼的操作也是，只要有变化就行，不需要过多幅度