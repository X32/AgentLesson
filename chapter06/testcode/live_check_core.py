# # 基础算法

import math, numpy as np

# 定义两个坐标点
# P1 = [10, 15]
# P5 = [12, 21]
#
# 使用标准的勾股定理计算两点之间的距离
# sum = (P1[0] - P5[0])**2 + (P1[1] - P5[1])**2
# distance = math.sqrt(sum)
# print(distance)
#
# 使用Numpy进行直接运算，不需要单独取出X和Y
# P1 = np.array(P1)
# P5 = np.array(P5)
# distance = np.sqrt(np.sum((P1 - P5)**2))
# print(distance)

# 使用math或numpy内置的函数直接计算
# print(math.dist(P1, P5))
# print(np.linalg.norm(P1-P5))


# 计算标准差和离散系数
ear = [0.35, 0.1, 0.15, 0.25, 0.4, 0.33, 0.16, 0.42]

# 使用公式进行计算
avg = math.fsum(ear)/len(ear)
sum = math.fsum([(x - avg)**2 for x in ear])
std = math.sqrt(sum/len(ear))
print(std/avg)

# 使用numpy直接计算
ratio = np.std(ear)/avg
print(ratio)


numbers = [0.1538275232589123,0.2407114441176289, 0.1415661409473635, 0.1737488687443733, 0.12979690024029544, 0.19267999459146032, 0.16915517838338234, 0.19429289738784067]
print(np.std(numbers))
print(np.average(numbers))
print(np.std(numbers) / np.average(numbers))







'''
以下定义了各个点对应的顺序，便于在后续代码中快速取得相对位置的下标
features = {
    "chin": points[0:17],              # 下巴或脸颊，对应下标为0~16共17个点，注意下标从0开始
    "left_eyebrow": points[17:22],   # 左眼眉，下标为17~21，与图6-10的人脸特征点编号要-1
    "right_eyebrow": points[22:27],  # 右眼眉
    "nose_bridge": points[27:31],    # 鼻梁
    "nose_tip": points[31:36],        # 鼻尖
    "left_eye": points[36:42],        # 左眼
    "right_eye": points[42:48],       # 右眼
    "top_lip": points[48:55] + [points[64]] + [points[63]] + [points[62]] + [points[61]] + [points[60]],                         # 上嘴唇，也可以细分上外嘴唇和上内嘴唇
    "bottom_lip": points[54:60] + [points[48]] + [points[60]] + [points[67]] + [points[66]] + [points[65]] + [points[64]]        # 下嘴唇，也可以细分上外嘴唇和上内嘴唇
}
'''


import face_recognition, cv2, time, numpy as np

# EAR计算，输入landmarks，输出EAR
def eye_aspect_ratio(landmarks):
    # 先取得左右眼的坐标值：[(482, 244), (497, 240), ... 共6个坐标]
    left_eye = np.array(landmarks[0]['left_eye'])
    right_eye = np.array(landmarks[0]['right_eye'])

    # 计算两个坐标点的距离：np.sqrt(np.sum((p1 - p2) ** 2))

    left_1_4 = np.linalg.norm(left_eye[0] - left_eye[3])
    left_2_6 = np.linalg.norm(left_eye[1] - left_eye[5])
    left_3_5 = np.linalg.norm(left_eye[2] - left_eye[4])
    left_ear = (left_2_6 + left_3_5) / (left_1_4 * 2)

    right_1_4 = np.linalg.norm(right_eye[0] - right_eye[3])
    right_2_6 = np.linalg.norm(right_eye[1] - right_eye[5])
    right_3_5 = np.linalg.norm(right_eye[2] - right_eye[4])
    right_ear = (right_2_6 + right_3_5) / (right_1_4 * 2)

    # 将两只眼睛的平均EAR值返回
    return (left_ear + right_ear) / 2

# 检测是否嘴巴的MAR值
def mouth_aspect_ratio(landmarks):
    # 'top_lip': 上嘴唇对应坐标与人脸点位编号：49, 50, 51, 52, 53, 54, 55, 65, 64, 63, 62, 61
    # 'bottom_lip': 下嘴唇对应编号为：55，56，57，58，59，60，49，61，68，67，66，65
    # 上嘴唇取62、63、64三个点（内嘴唇），对应下标为：top_lip[10], top_lip[9], top_lip[8]
    # 下嘴唇取68、67、66三个点（内嘴唇），对应下标为：bottom_lip[8], top_lip[9], top_lip[10]
    top_lip = np.array(landmarks[0]['top_lip'])
    bottom_lip = np.array(landmarks[0]['bottom_lip'])

    # 取下下嘴唇的三个内点进行计算，并求平均值
    # point_62_68 = np.linalg.norm(top_lip[10] - bottom_lip[8])
    # point_63_67 = np.linalg.norm(top_lip[9] - bottom_lip[9])
    # point_64_66 = np.linalg.norm(top_lip[10] - bottom_lip[8])
    # lip_width = np.linalg.norm(top_lip[0] - top_lip[6])
    # mar = (point_62_68 + point_63_67 + point_64_66) / (lip_width * 3)
    # return mar

    # 也可以只取上嘴唇的63和下嘴唇的67两个顶点进行计算，减少运算量
    point_63_67 = np.linalg.norm(top_lip[9] - bottom_lip[9])
    lip_width = np.linalg.norm(top_lip[0] - top_lip[6])
    return point_63_67 / lip_width


def nod_detect(landmarks):
    nose_tip = np.array(landmarks[0]['nose_tip'])
    chin = np.array(landmarks[0]['chin'])
    distance = np.linalg.norm(nose_tip[2] - chin[8])
    return distance

def camera_capture():
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        locations = face_recognition.face_locations(frame)
        if len(locations) > 0:
            print(f"检测到{len(locations)}张人脸")
            top, right, bottom, left = locations[0]  # 只取一张人脸
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), thickness=2)

            landmarks = face_recognition.face_landmarks(frame)
            # ear = eye_aspect_ratio(landmarks)
            # cv2.putText(frame, str(ear), (left - 5, bottom + 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), thickness=2)
            # mar = mouth_aspect_ratio(landmarks)
            # cv2.putText(frame, str(mar), (left - 5, bottom + 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), thickness=2)
            nod = nod_detect(landmarks)
            cv2.putText(frame, str(nod), (left - 5, bottom + 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), thickness=2)
        else:
            print("未检测到人脸")

        # 实时渲染摄像头数据，按q键退出
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.5)  # 间隔100毫秒渲染一次，也可以更快

    camera.release()  # 释放摄像头实例

# if __name__ == '__main__':
    # camera_capture()