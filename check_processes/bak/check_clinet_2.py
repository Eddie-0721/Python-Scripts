import subprocess

def check_exe_status(exe_path):
    try:
        # 启动.exe程序
        process = subprocess.Popen(exe_path)

        # 等待程序运行结束
        process.wait()

        # 检查返回码
        return_code = process.returncode
        if return_code == 0:
            return "正常"
        else:
            return "异常"
    except Exception as e:
        return str(e)

# 指定要检查的.exe程序路径
exe_path = 'D:\Local-Apps\金桥TRax交易终端\yl-jq-trader\金桥测试环境交易终端.exe'

# 检查程序状态
status = check_exe_status(exe_path)
print(f'程序状态：{status}')