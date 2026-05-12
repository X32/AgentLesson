import smtplib, time, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

# 发送邮件提醒的代码
def send_email(receiver, content, subject="新客户咨询提醒"):
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


def new_customer(contact_way, contact_type="未知"):
    content = f"有新的客户正在咨询，联系方式为：{contact_way}，类型为：{contact_type}"
    send_email("dengqiang@woniuxy.com", content)
    return "Mail-Sent"


# 声明函数及参数说明，注意中文描述要尽量准确，便于大模型理解
functions = [
{
    "type": "function",
    "function": {
        "name": "new_customer",
        "description": "识别出客户的联系方式和联系类型并通知接待",
        "parameters": {
            "type": "object",
            "properties": {
                "contact_way": {
                    "type": "string",
                    "description": "客户联系方式，可以是电话、手机号码、邮箱地址、微信号、QQ号等",
                },
                "contact_type": {
                    "type": "string",
                    "description": "客户的联系方式类型，如：电话、邮箱、微信等",
                }
            },
            "required": ["contact_way"]
        },
    }
}
]

# 对邮件发送功能进行测试
if __name__ == '__main__':
    # send_email("dengqiang@woniuxy.com", "祝你节日快乐，工作顺利。")
    new_customer("18812345678", contact_type="手机")