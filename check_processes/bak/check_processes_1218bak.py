import os
import smtplib
import socket
import logging
from logging.handlers import RotatingFileHandler
import subprocess
import psutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime

# 创建一个日志记录器
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# 创建一个文件处理器，设置日志文件路径和大小
log_file_path = 'E:\wiki\8_Python\check_processes\log\\check_processes_monitor.log'
max_bytes = 104857600  # 设置最大文件大小（字节数）
backup_count = 100  # 设置保留的备份文件数量
file_handler = RotatingFileHandler(log_file_path, maxBytes=max_bytes, backupCount=backup_count)
file_handler.setLevel(logging.DEBUG)

# 定义日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理器添加到日志记录器
logger.addHandler(file_handler)


# 要监控的脚本名称
script_name = 'appserver.py'
crash_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 发件人和收件人邮箱账号
my_sender = 'wenpeng.ouyang@infinitequant.cn'
my_user = ['jacksoulmate@163.com']
#'jiahui.liang@infinitequant.cn'
# user登录邮箱的用户名和密码
my_pass = 'AhPNd@jEa.7n!M4'

def send_email_script(script_name, crash_time):
    try:
        # 创建MIMEMultipart对象作为邮件容器
        message = MIMEMultipart()
        # 发件人、收件人信息
        message['From'] = formataddr(["", my_sender])
        message['To'] = formataddr(["", ', '.join(my_user)])
        # 邮件主题
        message['Subject'] = "紧急告警：appserver.py程序崩溃"

        content = f"""
尊敬的用户，您好

我们的监控系统检测到程序发生崩溃。以下是详细信息：

- 程序名称：[ {script_name} ]
- 运行主机：[ win10 192.168.0.122 ]
- 崩溃时间：[ {crash_time} ]
- 错误日志：[ {log_file_path} ]

我们的技术团队已经被通知，并将尽快处理这一问题。如果您有任何疑问或需要进一步的帮助，请及时与我们联系。

谢谢您的理解和支持。

此致
欧阳文鹏
实施工程师
部门名称：实施部
上海宇量智慧数据技术有限公司
Tel:+86：18075525253
E-mail：wenpeng.ouyang@infinitequant.cn
"""
        message.attach(MIMEText(content.strip(), 'plain'))

        # SMTP服务器
        smtp_server = "smtp.exmail.qq.com"
        smtp_port = 465

        # 连接SMTP服务器
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            # 登录服务器
            server.login(my_sender, my_pass)
            # 发送邮件给每个收件人
            for recipient in my_user:
                server.sendmail(my_sender, recipient, message.as_string())

        return True
    except Exception as e:
        logger.error("Email sent failed: %s", str(e))
        return False


def send_email_client(exe_name, crash_time):
    try:
        # 创建MIMEMultipart对象作为邮件容器
        message = MIMEMultipart()
        # 发件人、收件人信息
        message['From'] = formataddr(["", my_sender])
        message['To'] = formataddr(["", ', '.join(my_user)])
        # 邮件主题
        message['Subject'] = "紧急告警：交易端客户端崩溃"

        content = f"""
尊敬的用户，您好

我们的监控系统检测到程序发生崩溃。以下是详细信息：

- 程序名称：[ {exe_name} ]
- 运行主机：[ win10 192.168.0.122 ]
- 崩溃时间：[ {crash_time} ]
- 错误日志：[ {log_file_path} ]

我们的技术团队已经被通知，并将尽快处理这一问题。如果您有任何疑问或需要进一步的帮助，请及时与我们联系。

谢谢您的理解和支持。

此致
欧阳文鹏
实施工程师
部门名称：实施部
上海宇量智慧数据技术有限公司
Tel:+86：18075525253
E-mail：wenpeng.ouyang@infinitequant.cn
"""
        message.attach(MIMEText(content.strip(), 'plain'))

        # SMTP服务器
        smtp_server = "smtp.exmail.qq.com"
        smtp_port = 465

        # 连接SMTP服务器
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            # 登录服务器
            server.login(my_sender, my_pass)
            # 发送邮件给每个收件人
            for recipient in my_user:
                server.sendmail(my_sender, recipient, message.as_string())

        return True
    except Exception as e:
        logger.error("Email sent failed: %s", str(e))
        return False

def check_port(port):
    try:
        # 创建一个套接字对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 尝试连接到指定端口
        result = sock.connect_ex(('localhost', port))
        
        # 根据连接结果进行判断
        if result == 0:
            print(f"The script '{script_name}' is running.")
            return True  # 如果端口已打开，直接退出函数并返回True
        else:
            print(f"The script '{script_name}' is not running.")
        
        # 关闭套接字连接
        sock.close()
    except socket.error as e:
        logger.info(f"An error occurred while checking the port: {e}")


def start_client():
    exe_path = 'D:\Local-Apps\金桥TRax交易终端\yl-jq-trader'
    exe_pathname = 'D:\Local-Apps\金桥TRax交易终端\yl-jq-trader\金桥测试环境交易终端.exe'
    exe_name = os.path.basename(exe_pathname)
    # result = subprocess.run(exe_path, check=True)
    # if result.returncode == 0:
    os.chdir(exe_path)
    result = subprocess.Popen(exe_name)
    print(f"{result}")
    logger.info(f"The client {exe_name} start successfully.")
    # else:
    #     logger.error(f"The client {exe_name} start failed.")

exe_file = 'D:\Local-Apps\金桥TRax交易终端\yl-jq-trader\金桥测试环境交易终端.exe'
exe_name = os.path.basename(exe_file)
def check_client():
# 查找所有正在运行的进程
    for proc in psutil.process_iter(['name']):  
        # 检查进程是否为指定的exe文件  
        if proc.info['name'] == os.path.basename(exe_file):  
            # 如果进程是指定的exe文件，则打印进程信息并退出循环
            print(f"The client '{proc.info['name']}' is running.")
            logger.info(f"The client '{proc.info['name']}' is running.")  
            break  
    else:  
        # 如果循环结束时没有找到进程，则打印指定程序未运行的消息  
        logger.error(f"The client '{exe_name}' is not running")
        send_email_client(exe_name, crash_time)
        print(f"'{exe_name}' Alarm Email sent successfully.")
        logger.info(f"'{exe_name}' Alarm Email sent successfully.")
        start_client()


def start_script():
    script_name = 'appserver.py'
    script_path = 'C:\\Users\\LY-OuYang\\Desktop\\'
    # 构建命令行参数
    command = [r'C:\\Users\\LY-OuYang\AppData\\Local\\Programs\\Python\\Python310\\python.exe', script_path + script_name]
    try:
        # 创建STARTUPINFO对象并设置参数，使子进程在后台执行
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # 后台运行
        subprocess.Popen(command)
        # 前台运行
        #subprocess.run(command, check=True, startupinfo=startupinfo)
        #logger.info(f"Restart completed")
        logger.info(f"The script '{script_name}' started successfully.")
    except subprocess.CalledProcessError as e:
        logger.info(f"Failed to execute the script '{script_name}'. Error: {e}")



while True:
    # 检查客户端
    check_client()
    # 检查apiserver脚本和8088端口
    if check_port(8088):
        logger.info(f"The script '{script_name}' is running.")
    else:
        logger.error(f"The script '{script_name}' is not running.")
        #crash_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #if send_email_script(script_name, crash_time):
        print(f"'{script_name}' Alarm Email sent successfully.")
        logger.info(f"'{script_name}' Alarm Email sent successfully.")
        start_script()
        print("Done!")