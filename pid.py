import psutil


# 获取应用程序进程名称对应的pid
def get_pid(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            return proc.info['pid']


pid = get_pid('your_application_name')
print(pid)