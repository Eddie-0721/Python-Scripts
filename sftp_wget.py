# -*- coding: utf-8 -*-
import os
import subprocess
from datetime import datetime

# 版本说明
version="v1.0.20231102"
redeme="从shell版本修改为python版本，解决配置文件过多冗余的问题"

#当前目录配置（可默认）
current_dir="/home/yuliang/store"

#总线服务器获取算法商原始券池文件目录(自行配置)
original_dir="/home/yuliang/store"

#总线跑批任务高收益券池目录(自行配置)
stock_dir="/home/yuliang/store/stock_pool"

#SFTP服务器地址配置
url_sftp="https://222.71.222.250:65443"
params_sftp="--no-check-certificate"
sftpuser="--http-user=sftpalgo"
sftpasswd="--http-passwd=hw2dBxzB"

# 算法商算法高收益券池配置
files = [
    {
        "id": "1003",
        "name": "ngw1003",
        "sftpfile": "/ngw1003/niuguwang",
    },
    {
        "id": "1005",
        "name": "zc1005",
        "sftpfile": "/zc1005/zicheng",
    },
    {
        "id": "1006",
        "name": "hx1006",
        "sftpfile": "/hx1006/haoxing",
    },
    #{
        #############示例##############
        #"id": "算法商公司编码",
        #"name": "sftp算法商目录名称",
        #"sftpfile": "/sftp算法商目录名称/算法商名称全拼",
    #},   
]

# wget
def wget_files():
    for file in files:
        sftpfile = f"{file['sftpfile']}{datetime.now().strftime('%Y%m%d')}.csv"
        local_path = os.path.join(original_dir, f"{file['name']}{datetime.now().strftime('%Y%m%d')}.csv")
        stock_path = os.path.join(stock_dir, f"{file['id']}{datetime.now().strftime('%Y%m%d')}.csv")
        print(url_sftp,sftpfile,local_path,stock_path)
        result = subprocess.run(["/bin/wget", f"{url_sftp}{sftpfile}", "-O", local_path,params_sftp,sftpuser,sftpasswd ],stdout=subprocess.DEVNULL)
        print("request values",result)

        # if os.path.exists(local_path):
        #     if os.path.getsize(local_path) == 0:
        #         print("wget file：",local_path,"File is empty!\n regain!")
        # if result is None:
        #     # 如果命令执行失败，result 为 None
        #     print(f"[ERROR] wget execute failure!")
        #     exit(1)

        if result.returncode != 0:
            # 如果返回值不为 0，说明 wget 命令执行失败
            print(f"[ERROR] Execution failed or {stock_path} file does not exist!\n\n")
            try:
                os.remove(local_path)
            except OSError as e:
                print("ERROR remove info",e)
            continue
        else:
            print(f"[WGET]: {local_path} get time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            os.rename(local_path, stock_path)
            print(f"[RNAME]: {stock_path} renamed time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if result.returncode == 4:  # 404 ... ... 返回码
            # 如果返回值为 ... 4，说明文件未找到，跳过当前循环
            print(f"File not found: {local_path} 404")
            continue

# check
def check_files():
    for file in files:
        algo_name = f"{file['name']}"
        stock_path = os.path.join(stock_dir, f"{file['id']}{datetime.now().strftime('%Y%m%d')}.csv")
        if os.path.isfile(stock_path):
            print("Strategy name:",algo_name)
            print(f"local path: {stock_path} exist!")
            print("Wget Successful!\n")
        else:
            print("Strategy name:",algo_name)
            print(f"local path: {stock_path} not exist!")
            print("Wget failed!\n")

wget_files()
check_files()
