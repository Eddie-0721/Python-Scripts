import psutil

def is_process_running(process_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'].lower() == process_name.lower():
            return True
    return False

# 指定要检查的进程名
exe_name = '金桥测试环境交易终端.exe'
#exe_name = 'D:\Local-Apps\金桥TRax交易终端\yl-jq-trader\金桥测试环境交易终端.exe'
# 检查进程是否运行
if is_process_running(exe_name):
    print(f'{exe_name} 正在运行')
else:
    print(f'{exe_name} 未运行')