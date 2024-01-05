'''
Author       : OuYang
Date         : 2024-01-04 13:30:41
Version      : v1.0
LastEditors  : OuYang
LastEditTime : 2024-01-05 13:23:25
Description  : 使用WechatBot发送webhook消息-yullog告警
'''

import send_webhook_tools
import logging
import hashlib
import time
import alarm_template_webhook as alarm_template_webhook
from datetime import datetime

# log_file 建议与send_webhook_tools类保持一致
log_file = "/home/algo/quote/test/nohuo.log"

# 创建logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# 创建RotatingFileHandler对象
handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)

# 设置日志格式
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(message)s')
handler.setFormatter(formatter)

# 添加handler到logger
logger.addHandler(handler)


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
    Environment_name = "金桥环境"
    processes_name = "/home/algo/unily_share/unily_fenghe"
    log_path_5 = "/home/algo/unily_share/unily_fenghe/yullog"
    # interval_time 检查间隔时间s秒
    interval_time = 240

    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def check_string_in_file(file_path, target_string):
        with open(file_path, 'r') as file:
            last_four_lines = file.readlines()[-4:]
            for line in last_four_lines:
                if target_string in line:
                    print(f"4 line:\n {last_four_lines} \n")
                    return True
        return False

file_path = "/home/algo/unily_share/unily_fenghe/yullog/log.txt"
target_string_1 = "tick-entrust:ExchangeId=1"
target_string_2 = "tick-entrust:ExchangeId=2"
target_string_3 = "DepthMkdata1 ExchangeId=1"
target_string_4 = "DepthMkdata1 ExchangeId=2"

while(True):
    if is_between_time("09:10:00","13:00:00") or is_between_time("13:00:00","15:00:00"):
        if all(
            check_string_in_file(file_path, target_string)
            for target_string in [target_string_1, target_string_2, target_string_3, target_string_4]
        ):
            logging.info("Market log normal")
        else:
            logging.error("Abnormal quotation log")
            bot.send_markdown(alarm_template_webhook.markdown_5(alarm_template_webhook.get_local_ip(),alarm_template_webhook.get_system_info(),alarm_template_webhook.get_system_info(),Environment_name,current_time,processes_name,log_path_5))
        time.sleep(interval_time)

