import random
import sys
import threading
import time


def run1():
    try:
        # 随机数
        print(random.Random.randint(1, 10))
        time.sleep(5)
        1/0
        print('run1')
    except Exception as e:
        raise e
def run2():
    try:
        time.sleep(3)
        2/0
        print('run2')
    except Exception as e:
        raise e

if __name__ == '__main__':
    try:
        # 打印随机数

        print(random.Random.randint(10))
        t1 = threading.Thread(target=run1())
        t1.start()
        t2 = threading.Thread(target=run2())
        t2.start()
        t1.join()
        t2.join()
    except Exception as e:
        sys.exit(1)