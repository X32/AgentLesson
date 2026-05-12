import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

image = cv2.imread("../faces/conference-room.jpeg")
image_new = Image.fromarray(image)  # 转换为numpy数组
draw = ImageDraw.Draw(image_new)    # 实例化绘图对象
# 定义中文字体
font = ImageFont.truetype("simhei.ttf", 50, encoding="utf-8")
draw.text((200, 300), "你好中国", (255, 255, 255), font=font)
# 将图像转换为numpy数组并使用OpenCV进行显示或保存
cv2.imshow("Image", np.array(image_new))
cv2.waitKey(0)


