# coding=utf-8

import os
import time
import smtplib
from email.mime.text import MIMEText

# 本来采用的是 schedule 库轮询系统时间实现定时功能
# 但测试发现 windows 系统下采用 python 库定时容易出现 异常 从而崩溃
# 因此改用 win10 自带 的 计划任务功能， python 端只实现adb通过 端口连接启动安卓端打卡辅助程序
# 自带的 计划任务 很好用，可以获取很多权限（例如定时开机 关机 管理员权限等等）
# 另外，使用 C# 配合 Quartz 理论上也可以实现windows 计划任务，但开发中遇到不明原因太多，不折腾所以直接用 py_installer 转换 py 到 exe
interval = 0

# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # SMTP服务器
mail_user = "dakaxiaozhushou@163.com"  # 用户名
mail_pass = "Cch13535"  # 授权密码，非登录密码

sender = 'dakaxiaozhushou@163.com'  # 发件人邮箱地址
receiver = '953633450@qq.com'  # 接受端邮箱地址 由于发群发会造成垃圾邮件被服务器拒绝 所以不采用 [] ，直接单发

content = '不用回复'
title = '打卡在python端执行了， 执行时间为' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 邮件主题


def send_email():  # 调用 smtplib 发送邮件
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = 'dakaxiaozhushou@163.com'
    message['To'] = '953633450@qq.com'
    message['Subject'] = title

    try:
        smtpobj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口 465 996 都可行
        smtpobj.login(mail_user, mail_pass)  # 登录验证
        smtpobj.sendmail(sender, receiver, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)


def check_in():  # 主要操作 启动 安卓端的 auto check in app， 进行一次打卡操作
    print('上一次打卡时间为:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    os.system('adb kill-server')  # 测试时发现 先kill-server 可以避免启动服务器失败的情况，可以理解为一个 初始化操作，保证一切关闭
    os.system('adb start-server')  # 这句可以省略，因为执行 adb 命令后 服务器会自动启动
    print("start check-in")
    os.system('adb root')  # get superuser
    time.sleep(1)
    os.system(
        'adb shell am start -n ' + 'com.tommy.autocheckin' +  # 留意保证合适的 空格 断句
        '/' + 'com.tommy.autocheckin.ui.MainActivity')  # 打开 autocheckin， MainActivity 是入口


if __name__ == "__main__":  # 入口
    send_email()  # 发送提醒邮件
    check_in()  # 通过adb 发送intent 启动打卡app 的main activity 执行打卡操作
