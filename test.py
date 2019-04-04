#!C:\Users\Administrator\PycharmProjects\untitled\venv
# -*- coding:utf-8 -*-

# import subprocess
#
# obj = subprocess.Popen('sichuan.py',shell=True)
#
# print(111)
# print(111)
# print(111)
# print(111)

# import json
# from multiprocessing import Process, Lock, Queue
# from time import sleep
# import os
# myn = 11
#
# def run(n, lock):
#     lock.acquire()
#     global myn
#     myn += n
#     print(myn)
#     lock.release()
# if __name__ == "__main__":
#     print("主进程开始执行%s" % (os.getpid()))
#     lock = Lock()
#     for i in range(5):
#         p = Process(target=run, args=(i,lock))
#         p.start()
#     print(myn)

import multiprocessing
import time

'''一个进程模拟写数据'''
myn = 0

def data_file(q, i):
    q.put(i)


'''一个进程模拟处理数据'''


def modify_data(q):
    global myn
    while 1:
        i = q.get()
        myn += i
        print(myn)

def main():
    # 创建一个队列、
    q = multiprocessing.Queue()

    '''创建多个进程，将队列的引用当做实参进行传递到里面'''
    for i in range(5):
        p1 = multiprocessing.Process(target=data_file, args=(q,i))
        p1.start()
    p2 = multiprocessing.Process(target=modify_data, args=(q,))

    p2.start()


if __name__ == '__main__':
    main()



