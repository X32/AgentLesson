import smtplib, time, os    # smtplib模块主要用于处理SMTP协议
# email模块主要处理邮件的头和正文等数据
# from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()


def send_email(receiver, content, subject=None):
    sender = '15903523@qq.com'  # 发送邮箱

    # 构建邮件的主体对象
    msg = MIMEMultipart()

    if subject is not None:
        msg['Subject'] = subject
    else:
        msg['Subject'] = f"来自{sender}的问候邮件"
    msg['From'] = sender
    msg['To'] = receiver

    # 构建邮件的正文内容# 构建邮件的正文内容
    body = MIMEText(content, 'html', 'utf-8')
    msg.attach(body)

    # 建立与邮件服务器的连接并发送邮件
    smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)   # 如果基于SSL，则 smtplib.SMTP_SSL
    smtpObj.login(user=sender, password=os.getenv("QQ_Mail_Password"))
    smtpObj.sendmail(sender, receiver, str(msg))
    smtpObj.quit()

    return "邮件已经成功发送到：" + receiver


# 系统级提示词
system_prompt = """
	你是一名AI助手，具备函数调用的能力，但是如果提供的信息已经足够回答用户的问题，则不需要再进行函数调用。
	同时，请严格按照函数调用的方式进行处理，如果用户未提供函数所需参数，则必须询问，而不能自作主张。
"""

# 声明函数及参数说明，注意中文描述要尽量准确，便于大模型理解
functions = [
{
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "向指定邮箱地址发送一封邮件",
        "parameters": {
            "type": "object",
            "properties": {
                "receiver": {
                    "type": "string",
                    "description": "邮件的收件地址",
                },
                "content": {
                    "type": "string",
                    "description": "邮件的正文内容，支持HTML格式",
                },
                "subject": {
                    "type": "string",
                    "description": "邮件的标题，如果没有标题，可以设置为空",
                },
            },
            "required": ["receiver", "content"]
        },
    }
}
]

# 对邮件发送功能进行测试
if __name__ == '__main__':
    send_email("dengqiang@woniuxy.com", "祝你节日快乐，工作顺利。")