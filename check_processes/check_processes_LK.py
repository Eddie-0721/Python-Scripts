import os
import smtplib
import socket
import logging
import time
import syncScript2
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
import subprocess
import psutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime


################### 配置信息 ###################
# appserver
script_name = 'appserver.py'
script_path = 'C:\\yl_tfzq_client\\yl-term-trader\\'
script_port = '8088'

# 券商交易客户端
exe_name = "天风证券交易终端.exe"
exe_path_name = "C:\yl_tfzq_client\yl-term-trader\天风证券交易终端.exe"
#exe_path = "D:\Local-Apps\金桥TRax交易终端\yl-jq-trader"

# 发件人和收件人邮箱账号
my_sender = 'wenpeng.ouyang@infinitequant.cn'
my_user = ['jacksoulmate@163.com']
# user登录邮箱的用户名和密码
my_pass = 'AhPNd@jEa.7n!M4'

# 日志文件
log_file_path = 'C:\\yl_tfzq_client\\check_processes\\log\\monitor.log'
# python执行exe目录
python_local_path = 'C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python310\\python.exe'
################### END ###################


# 创建一个日志记录器
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# max_bytes = 10485760  # 设置最大文件大小（字节数）
# backup_count = 100  # 设置保留的备份文件数量
#file_handler = RotatingFileHandler(log_file_path, maxBytes=max_bytes, backupCount=backup_count,encoding='utf-8')
file_handler = RotatingFileHandler(log_file_path,encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# 创建一个每天滚动的日志文件
logging_handler = TimedRotatingFileHandler(log_file_path, when='midnight')

# 定义日志格式
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理器添加到日志记录器
logger.addHandler(file_handler)

# 客户端
#exe_name = os.path.basename(exe_path_name)
exe_path = os.path.dirname(exe_path_name)

# appserver
#script_name = os.path.basename(script_path)


crash_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def send_email_script(script_name):
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
                logger.info(f"'{script_name}' Alarm Email sent successfully.")

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
                logger.info(f"'{exe_name}' Alarm Email sent successfully.")

        return True
    except Exception as e:
        logger.error("Email sent failed: %s", str(e))
        return False


def start_script(script_path,script_name):
    bat_script = f'''
    @echo off
    cd /d {script_path}
    start pythonw {script_name}
    '''

    # 将批处理命令写入临时文件
    bat_file = 'temp.bat'
    with open(bat_file, 'w') as f:
        f.write(bat_script)
    # 执行批处理命令
    subprocess.call([bat_file], shell=True)
    # 删除临时文件
    subprocess.call(['del', bat_file], shell=True)
    subprocess.check_output
    #logger.info(f"The client '{exe_name}' start successfully.")
    print(f"start {script_name}")

def check_port(port):
    try:
        # 创建一个套接字对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 尝试连接到指定端口
        result = sock.connect_ex(('localhost', port))
        # 根据连接结果进行判断
        if result == 0:
            #print(f"The script '{script_name}' is running.")
            logger.info(f"The script '{script_name}' is running.")
            return True  # 如果端口已打开，直接退出函数并返回True
        else:
            #print(f"The script '{script_name}' is not running.")
            logger.error(f"The script '{script_name}' is not running.")
            send_email_script(script_name)
            kill_process_by_port(script_port)
            start_script(script_path,script_name)
            pass
        
        # 关闭套接字连接
        sock.close()
    except socket.error as e:
        logger.info(f"An error occurred while checking the port: {e}")


def kill_process_by_port(port):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.name() == 'pythonw.exe':
            try:
                connections = proc.connections()
                for conn in connections:
                    if conn.laddr.port == port:
                        proc.terminate()
                        print('Process with port {} terminated.'.format(port))
                        return
            except psutil.NoSuchProcess:
                pass

    print('No process found with port {}.'.format(port))

# def start_client(client):
#     exe_name = os.path.basename(exe_path_name)
#     os.chdir(exe_path)
#     global result
#     result = subprocess.Popen(exe_path_name)
#     logger.info(f"The client '{exe_name}' start successfully.")
        
def start_client(client_path,client_name):
    bat_script = f'''
    @echo off
    cd /d {client_path}
    start {client_name}
    '''

    # 将批处理命令写入临时文件
    bat_file = 'temp.bat'
    with open(bat_file, 'w') as f:
        f.write(bat_script)
    # 执行批处理命令
    subprocess.call([bat_file], shell=True)
    # 删除临时文件
    subprocess.call(['del', bat_file], shell=True)
    subprocess.check_output
    logger.info(f"The client '{exe_name}' start successfully.")
    


    
def check_client(client):
# 查找所有正在运行的进程
    for proc in psutil.process_iter(['name']):  
        # 检查进程是否为指定的exe文件  
        if proc.info['name'] == os.path.basename(client):  
            # 如果进程是指定的exe文件，则打印进程信息并退出循环
            #print(f"The client '{proc.info['name']}' is running.")
            logger.info(f"The client '{proc.info['name']}' is running.")  
            check_sync()
            break
    else:  
        # 如果循环结束时没有找到进程，则打印指定程序未运行的消息  
        logger.error(f"The client '{exe_name}' is not running")
        send_email_client(exe_name, crash_time)
        #print(f"'{exe_name}' Alarm Email sent successfully.")
        #logger.info(f"'{exe_name}' Alarm Email sent successfully.")
        start_client(exe_path,exe_name)
        time.sleep(5)

def close_client(exe_name):
   logger.info(f"Closing the '{exe_name}' client.")
   kill_cmd = f"taskkill /IM {exe_name} /F"
   subprocess.run(kill_cmd,shell=True)


def check_sync():
    brokercode = syncScript2.traverseBrokerCode(["tfzq"])
    print(f"traverseBrokerCode_result: {brokercode}")
    for k, v in brokercode.items():
        if k == "tfzq":
            if v:
                logger.info("Client Normal synchronization.")
                break
            else:
                logger.error("The client synchronization is disconnected.")
                close_client(exe_name)
                os.chdir(exe_path)
                start_client(exe_path,exe_name)
                logger.info("The client is restarted successfully.")



if __name__== "__main__" :
    check_client(exe_path_name)
    check_port(8088)
    logger.info("Check Done!")