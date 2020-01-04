#!/usr/bin/python
# -*- coding: UTF-8 -*-

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 发件人地址
from_addr = 'fuzp@253.com'
# 邮箱密码
password = 'Asdf93310'
# 收件人地址
to_addr = 'fuzp@253.com'
# 邮箱服务器地址
smtp_server = 'smtp.exmail.qq.com'

# 设置邮件信息
msg = MIMEMultipart()
msg['From'] = _format_addr('发件人<%s>' % from_addr)
msg['TO'] = _format_addr('收件人<%s>' % to_addr)
msg['Subject'] = Header('邮件主题', 'utf-8').encode()

# 邮件正文内容
msg.attach(MIMEText('你好，这是正文', 'plain', 'utf-8'))

# 构造附件1，传送当前目录下的 hbase_error.log 文件
att1 = MIMEText(open('./hbase_error.log', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="fujian.log"'
msg.attach(att1)

# 发送邮件
try:
    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
