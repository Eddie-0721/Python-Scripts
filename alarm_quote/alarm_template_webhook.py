'''
Author       : OuYang
Date         : 2023-12-28 18:00:26
LastEditTime: 2024-01-05 15:04:40
Description  : webhook消息模板
'''

import send_webhook_tools
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


def markdown_1(ip,filename,filetime,time,shell_name,logfile):
    """
    总线绩效评估文件同步成功消息模板
    """
    markdown_1 = f"""
        **总线绩效评估文件同步成功**
            >主机：{ip}
            >文件名称：{filename}
            >文件时间：{filetime}
            >时间：{time}
            >来源：{shell_name}
            >日志文件：{logfile}
    """
    return markdown_1

def markdown_2(ip,time,shell_name,remote_host,logfile):
    """
    行情cpxx文件同步失败消息模板
    """
    markdown_2 = f"""
        **cpxx文件同步失败**
            >主机：{ip}
            >时间：{time}
            >来源：{shell_name}
            >远端主机：{remote_host}
            >远端日志：{logfile}
    """
    return markdown_2

def markdown_3(Environment_name,ip,time):
    """
    ATM环境 落盘行情L1数据同步失败消息模板
    """
    markdown_3 = f"""
        ** [{Environment_name}] 落盘行情L1数据同步失败**
            >主机：{ip}
            >时间：{time}
            >远端主机：192.168.30.3
            >来源：sshfs
    """
    return markdown_3

def markdown_4(ip,sys_info,Environment_name,time,procedure,market_path,condition):
    """
    金桥环境 落盘行情异常情况消息模板
    """
    markdown_4 = f"""
        **[{Environment_name}] 落盘行情异常**
            >主机：{ip} {sys_info}
            >时间：{time}
            >落盘程序：{procedure}
            >落盘文件: {market_path}
            >触发条件：{condition}
    """
    return markdown_4


def markdown_5(ip,sys_info,Environment_name,time,processes_name,log_path_5):
    """
    金桥环境 转发行情日志异常情况消息模板
    """
    markdown_5 = f"""
        **[{Environment_name}] 转发行情**
            >主机：{ip} {sys_info}
            >时间：{time}
            >程序名：{processes_name}
            >日志目录：{log_path_5}
    """
    return markdown_5

def get_function_name(function_name:str):
    return function_name

def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    md5_hash = hashlib.md5(content).hexdigest()
    return md5_hash


# if __name__ == '__main__':
#     # 正式环境
#     #webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b726cce0-9aff-4392-b993-f226b76db022"
#     # 测试环境
#     webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4df4a188-084a-4866-afef-1df388f194de"
#     bot = send_webhook_tools.WechatBot(webhook_url)

#     ## 落盘行情监控配置参数 ##
#     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     market_path = "/home/algo/quote/20240102"
#     procedure = "/home/algo/yulcatchmd"
#     Environment_name = "金桥环境"
#     condition = "1分钟检查一次csv的MD5值是否相同，相同则发送告警"
#     interval_time = ""
#     ## end ##

#     def check_file_md5(directory):
#         """
#         检查落盘文件csv文件MD5值
#         """
#         md5_dict = {}
#         while True:
#             for file in os.listdir(directory):
#                 file_path = os.path.join(directory, file)
#                 if os.path.isfile(file_path) and file.endswith(".sz.csv"):
#                     md5 = calculate_md5(file_path)
#                     if file_path in md5_dict:
#                         if md5_dict[file_path] == md5:
#                             logging.error(f"Error: MD5 of file {file_path} has not changed!")
#                             bot.send_markdown(markdown_4(get_local_ip(),Environment_name,current_time,procedure,file_path,condition))
#                     md5_dict[file_path] = md5
#                     logging.info(f"File: {file_path}, MD5: {md5}")
#                 if os.path.isfile(file_path) and file.endswith(".sh.csv"):
#                     md5 = calculate_md5(file_path)
#                     if file_path in md5_dict:
#                         if md5_dict[file_path] == md5:
#                             logging.error(f"Error: MD5 of file {file_path} has not changed!")
#                             bot.send_markdown(markdown_4(get_local_ip(),Environment_name,current_time,procedure,file_path,condition))
#                     md5_dict[file_path] = md5
#                     logging.info(f"File: {file_path}, MD5: {md5}")
#             nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             logging.info(f"Time: {nowtime}")
#             time.sleep(interval_time)
        

#     check_file_md5(market_path)
    
    
    # filename = "E:\\wiki\\8_Python\\check_processes\\appserver.py"
    
    # # markdown1
    # bot.send_markdown(markdown_1(get_local_ip(),"testfile.txt",get_file_info(filename),time,shell_name="1.py",logfile="1.log"))

    # # markdown2
    # bot.send_markdown(markdown_2(get_local_ip(),time,shell_name="sshfs",remote_host="国新机房",logfile="null"))
    # logging.info(f"template: {get_function_name(function_name='markdown_2')} send message succeeded.")

    # markdown3
    #bot.send_markdown(markdown_3(Environment_name="献平ATM环境"),get_local_ip(),time)
    # bot.send_markdown(markdown_3("献平ATM环境", get_local_ip() ,time))
    #bot.send_markdown(markdown_3(get_local_ip(),time,Environment_name="献平ATM环境"))

    # # text1
    # bot.send_text("你好，这是一个测试！",['欧阳文鹏'],['18075525253'])
    