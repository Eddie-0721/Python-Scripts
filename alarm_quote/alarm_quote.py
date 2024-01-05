'''
Author       : OuYang
Date         : 2024-01-04 10:45:29
Version      : v1.0
LastEditors  : OuYang
LastEditTime : 2024-01-05 13:18:47
Description  : 使用WechatBot发送webhook消息-quote告警
'''


import send_webhook_tools
import alarm_template_webhook as alarm_template_webhook
import os
import platform
import socket
import inspect
import logging
import hashlib
import time
from datetime import datetime

# log_file 建议与send_webhook_tools类保持一致
log_file = "/home/algo/quote/test/nohuo.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='[%(asctime)s] - [%(levelname)s] - %(message)s')


def get_system_info():
    # 获取os信息
    #os_name = platform.platform()
    # 获取os类型
    os_type = platform.system()
    return os_type

def get_file_info(file_name:str):
    ctime = os.path.getctime(file_name) #创建时间
    ctime_string = datetime.fromtimestamp(int(ctime))
    mtime = os.path.getmtime(file_name) #修改时间
    mtime_string = datetime.fromtimestamp(int(mtime))
    # print(
    # f"创建时间：{ctime_string}", 
    # f"修改时间：{mtime_string}", 
    # sep="\n")
    return mtime_string

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_function_name(function_name:str):
    return function_name

def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    md5_hash = hashlib.md5(content).hexdigest()
    return md5_hash

def is_between_time(begin_time, end_time):
 
    now = time.strftime('%H:%M:%S')
    if begin_time <= now <= end_time:
        return True
    else:
        return False


if __name__ == '__main__':
    # 正式环境
    #webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b726cce0-9aff-4392-b993-f226b76db022"
    # 测试环境
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4df4a188-084a-4866-afef-1df388f194de"
    bot = send_webhook_tools.WechatBot(webhook_url)

    ## 落盘行情监控配置参数 ##
    current_date = time.strftime('%Y%m%d')
    market_path = f"/home/algo/quote/{current_date}"
    procedure = "/home/algo/yulcatchmd"
    Environment_name = "金桥环境"
    condition = "两分钟检查一次csv的MD5值是否相同，相同则发送告警"
    interval_time = 120
    ## end ##

    def check_file_md5(directory):
        """
        检查落盘文件csv文件MD5值
        """
        md5_dict = {}
        while True:
            if is_between_time("09:10:00","13:00:00") or is_between_time("13:00:00","15:00:00"):
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path) and file.endswith(".sz.csv"):
                        md5 = calculate_md5(file_path)
                        if file_path in md5_dict:
                            if md5_dict[file_path] == md5:
                                logging.error(f"Error: MD5 of file {file_path} has not changed!")
                                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                bot.send_markdown(alarm_template_webhook.markdown_4(get_local_ip(),alarm_template_webhook.get_system_info(),Environment_name,current_time,procedure,file_path,condition))
                        md5_dict[file_path] = md5
                        logging.info(f"File: {file_path}, MD5: {md5}")
                    if os.path.isfile(file_path) and file.endswith(".sh.csv"):
                        md5 = calculate_md5(file_path)
                        if file_path in md5_dict:
                            if md5_dict[file_path] == md5:
                                logging.error(f"Error: MD5 of file {file_path} has not changed!")
                                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                bot.send_markdown(alarm_template_webhook.markdown_4(get_local_ip(),alarm_template_webhook.get_system_info(),Environment_name,current_time,procedure,file_path,condition))
                        md5_dict[file_path] = md5
                        logging.info(f"File: {file_path}, MD5: {md5}")
                nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.info(f"Time: {nowtime}")
            time.sleep(interval_time)
        

    check_file_md5(market_path)