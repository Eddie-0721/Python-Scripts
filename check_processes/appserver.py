"""
本程序用于中转请求
"""
import asyncio
import json
import logging
import os.path
import threading
import time
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import setproctitle
import win32api
import websockets

# 设置本程序的进程名(程序会自动拼接程序绝对路径, 本程序和客户端一一对应, 名字最好能区分客户端的用户)
PROC_TITLE = "APPSERVER_001"
# 设置能够连接此服务的IP, 0.0.0.0表示无限制
IP_ADDR = '0.0.0.0'
# 服务端口
IP_PORT = 8088

# 接收请求, 写入的文件
INPUT_FILE_NAME_TEMPLATE = "./store/yl-term-request-{}.dat"
# 响应数据文件
OUTPUT_FILE_NAME_TEMPLATE = "./store/yl-term-result-{}.dat"
# 文件请求数据行结束标志, 只有含有此标志的数据才认为是合法的数据
LINE_END_SYMBOL = '\x03'

# 记录最后一次文件读取到的位置
start_index = 0
current_response_file = ""
# 从本次启动到当前接收请求个数
total_msg_num = 0
# 记录发送的请求响应个数
send_num = 0

lock = asyncio.Lock()

# 创建一个logger
logger = logging.getLogger('ts')
logger.setLevel(logging.DEBUG)

# 创建一个每天滚动的日志文件
logging_handler = TimedRotatingFileHandler('appserver.log', when='midnight')

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logging_handler.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(logging_handler)


class ConnectionService:
    """
    管理websocket连接信息
    """
    connection_data = None

    def __init__(self):
        self.connection_data = {}
        self.start_monitor()

    def add_request(self, request_id, ws):
        self.connection_data[request_id] = ws
        logger.debug("add one request, total: %s, request_id: %s, connection: %s", len(self.connection_data.keys()),
                     request_id, ws.id)

    def remove_request(self, request_id):
        ws = self.connection_data.get(request_id)
        del self.connection_data[request_id]
        logger.debug("remove one request, total: %s, request_id: %s, connection: %s", len(self.connection_data.keys()),
                     request_id, ws.id)

    async def send_message(self, request_id, message):
        ws = self.connection_data.get(request_id)
        if ws:
            async with lock:
                await ws.send(message)
                self.remove_request(request_id)

    def close(self, ws):
        """
        释放所有已经断开的连接缓存
        """
        request_ids = [_id for (_id, value) in self.connection_data.items() if value == ws]
        logger.debug("close one connection: %s, start...", ws.id)
        for request_id in request_ids:
            self.remove_request(request_id)

        logger.debug("close one connection: %s, complete...", ws.id)

    def start_monitor(self):
        """
        监控连接是否断开, 如果断开了, 则关闭此连接的所有缓存, 防止内存溢出
        """

        def run(*args):
            while True:
                try:
                    for request_id in list(self.connection_data.keys()):
                        ws = self.connection_data.get(request_id)
                        if ws and ws.closed:
                            self.close(ws)
                except Exception as e:
                    logger.error("关闭无效链接错误", exc_info=True)
                finally:
                    time.sleep(10)

        threading.Thread(target=run).start()


connectionService = ConnectionService()


async def message_handler(websocket, path):
    try:
        await receive_message(websocket, path)
    except Exception as e:
        logger.error("处理请求异常", exc_info=True)
    finally:
        logger.info("connection is closed")


async def receive_message(connect, path):
    """ 接收客户端的请求, 并把请求信息写入文件 """
    global total_msg_num

    async for message in connect:
        try:
            if not message:
                continue

            total_msg_num = total_msg_num + 1

            # 心跳
            if "\"oper\": \"touch\"" in message:
                pass
            else:
                logger.debug("receive, total: %s, msg: %s", total_msg_num, message)
                event = json.loads(message)
                request_id = event.get("requestId")

                # 只有有request_id才是正常的请求
                if request_id:
                    connectionService.add_request(request_id, connect)
                    await write_request_to_file(message)
        except Exception as e:
            logger.error('handle request message error', exc_info=True)


async def write_request_to_file(api_info):
    """ 把请求信息写入文件 """
    request_file = get_file_name(INPUT_FILE_NAME_TEMPLATE)
    with open(request_file, 'at', encoding="utf-8") as file:
        # 以END为结束符
        file.write(api_info + LINE_END_SYMBOL + "\n")


async def handle_response():
    """ 读取响应文件, 把响应数据发送出去 """
    # 程序启动时把初始读取位置设为文件末尾
    global start_index
    global current_response_file

    # 程序启动时进入此方法, 记录此时的文件名, 如果文件存在, 则从文件的末尾开始读取数据, 之前的数据丢弃
    current_response_file = get_file_name(OUTPUT_FILE_NAME_TEMPLATE)
    if os.path.exists(current_response_file):
        start_index = os.path.getsize(current_response_file)

    while True:
        try:
            response_file = get_file_name(OUTPUT_FILE_NAME_TEMPLATE)

            # 如果到新的一天了, 更新当前文件名称和待读数据的位置
            if current_response_file != response_file:
                start_index = 0
                current_response_file = response_file

            if os.path.exists(current_response_file):
                await read_and_send(current_response_file)
        except Exception as e:
            logger.error("读取响应文件错误", exc_info=True)
        finally:
            await asyncio.sleep(1)


async def read_and_send(response_file):
    """ 从响应文件中读取结果并发送给请求方 """

    global start_index
    global current_response_file
    with open(response_file, "r+", encoding='utf-8') as fo:
        fo.seek(start_index, 0)

        cache_char = ""
        read_num = 1
        while True:
            response_file = get_file_name(OUTPUT_FILE_NAME_TEMPLATE)

            # 如果到新的一天了, 则退出循环
            if current_response_file != response_file:
                break

            # 一次读取1M数据
            line_data = fo.read(1048576)
            # 把上次没有处理完的数据拼接
            if line_data:
                logger.debug("read chunk: %s", read_num)
                cache_char = cache_char + line_data
            else:
                # 没有读取到数据, 则先sleep 1秒
                await asyncio.sleep(1)
                continue

            end_index = cache_char.rfind(LINE_END_SYMBOL)
            if end_index != -1:
                read_num = 1
                temp_char = cache_char[:end_index]
                cache_char = cache_char[end_index + 2:]
            else:
                read_num = read_num + 1
                continue

            responses = temp_char.split(LINE_END_SYMBOL + '\n')
            await send_response(responses)


async def send_response(responses):
    """ 发送相应给客户端 """
    global send_num
    for line in responses:
        send_num = send_num + 1
        try:
            if line and (line.startswith("{") or line.startswith("\n{")):
                response = json.loads(line)
                request_id = response.get("requestId")
                await connectionService.send_message(request_id, line)
            else:
                logger.debug("send one response, not complete line: %s", line)
        except:
            logger.error("send one response error, data: %s", line, exc_info=True)
        finally:
            logger.debug("send one response, total: %s, line: %s", send_num, line)


def get_file_name(template):
    return template.format(datetime.now().strftime("%Y%m%d"))


async def run_server():
    # start a websocket server
    async with websockets.serve(message_handler, IP_ADDR, IP_PORT, ping_interval=None):
        await asyncio.Future()  # run forever


async def start():
    logger.info("request server is starting...")
    task_run_server = asyncio.create_task(run_server())
    handle_response_task = asyncio.create_task(handle_response())

    await task_run_server
    await handle_response_task


if __name__ == '__main__':
    # setproctitle.setproctitle(PROC_TITLE)
    asyncio.run(start())
