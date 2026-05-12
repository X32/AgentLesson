import base64

# # 读取二进制文件并输出Base64编码
# with open("./AI.jpg", "rb") as f:
#     content = f.read()
#
# b64str = base64.b64encode(content).decode()
# print(b64str)
#
# # 将Base64编码的字符串保存为二进制文件
# with open("./AI2.jpg", "wb") as f:
#     f.write(base64.b64decode(b64str))

print(base64.b64encode(b'Red'))