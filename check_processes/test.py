import syncScript2
import subprocess
import psutil
import time

# brokercode = syncScript2.traverseBrokerCode(["tfzq"])

# print(f"result: {brokercode}")

# for k, v in brokercode.items():
#     print(f"k is {k}，v is {v}")
#     if k == "tfzq":
#         if v:
#             print("True")
#         else:
#             print("False")

def start_client(client_path,client_name):
    bat_script = f'''
    @echo off
    cd /d {client_path}
    start pythonw {client_name}
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
    print(f"start {client_name}")


client_path = 'E:\wiki\8_Python\check_processes'
client_name = 'appserver.py'



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

# 指定要终止的端口号
port = 8088


kill_process_by_port(port)
start_client(client_path,client_name)
time.sleep(5)
# 终止对应的进程
kill_process_by_port(port)