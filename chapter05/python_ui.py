import tkinter as tk
from tkinter import *

# 界面绘制
root = tk.Tk()    # 实例化tkinter，作为主容器使用
root.title("智能语音记分牌")
# 表示容器大小为1020*600，启动时位于屏幕的（200,100)位置处（屏幕左上方顶点为原点）
root.geometry("1020x600+200+100")

# 添加Label元素，通常用于表示提示性文字
label_red = Label(root, text="红队(  )", font=('宋体',55), fg="#FF3300")
# place函数表示绝对定位，该元素位于容器原点（90，30）位置处
label_red.place(x=90, y=30)

label_red_score = Label(root, text="0", font=('宋体',70), fg="#FF3300")
label_red_score.place(x=290, y=25)

label_blue = Label(root, text="蓝队(  )", font=('宋体',55), fg="#3333FF")
label_blue.place(x=630, y=30)

label_blue_score = Label(root, text="0", font=('宋体',70), fg="#3333FF")
label_blue_score.place(x=830, y=25)

label_log = Label(root, text="两队得分记录", font=('宋体', 20), fg="green")
label_log.place(x=420, y=100)

# Entry表示文本框，用于记录两队的当局分数
entry_red = Entry(root, width=3, justify=CENTER, font=('宋体',80), fg="#FF3300")
entry_red.insert(0, "0")
entry_red.place(x=140, y=250)

entry_blue = Entry(root, width=3, justify=CENTER, font=('宋体',80), fg="#3333FF")
entry_blue.insert(0, "0")
entry_blue.place(x=720, y=250)

# Button为按钮，command参数绑定单击事件
button_end = Button(root, text=" 结束本局 ", width=9, font=('宋体',22), command=lambda: end_game())
button_end.place(x=150, y=500)

button_end = Button(root, text=" 开始本局 ", width=9, font=('宋体',25), bg="#33AA00", command=lambda: start_game())
button_end.place(x=425, y=500)

button_end = Button(root, text=" 撤消得分 ", width=9, font=('宋体',22), command=lambda: undo_score())
button_end.place(x=700, y=500)

button_red_plus = Button(root, text="+", width=3, font=('宋体',30), command=lambda: red_plus(1))
button_red_plus.place(x=190, y=150)

button_red_minus = Button(root, text="-", width=3, font=('宋体',30), command=lambda: red_minus(1))
button_red_minus.place(x=190, y=390)

button_blue_plus = Button(root, text="+", width=3, font=('宋体',30), command=lambda: blue_plus(1))
button_blue_plus.place(x=760, y=150)

button_blue_minus = Button(root, text="-", width=3, font=('宋体',30), command=lambda: blue_minus(1))
button_blue_minus.place(x=760, y=390)

# Text为文本域，用于记录得分日志
text_log = Text(root, height=14, width=24, font=('宋体',16))
text_log.place(x=380, y=160)

# 主线程正常启动UI界面
root.mainloop()
