#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import shlex

# shell 状态常亮
SHELL_STATUS_RUN = 1
SHELL_STATUS_STOP = 0

def tokenize(string):
    return shlex.split(string)

def execute(cmd_tokens):
    # 创建新进程执行命令
    pid = os.fork()

    if pid == 0: # 子进程
        # 执行命令
        os.execvp(cmd_tokens[0], cmd_tokens)
    elif pid > 0: # 父进程
        while True:
            # 等待其子进程的响应状态
            wpid, status = os.waitpid(pid, 0)

            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break

    return SHELL_STATUS_RUN

    # 返回状态等待下一条命令
    return SHELL_STATUS_RUN

def shell_loop():
    # 主循环
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        # 显示命令提示符
        sys.stdout.write('> ')
        sys.stdout.flush()

        # 读取命令输入
        cmd = sys.stdin.readline()

        # 切分命令输入
        cmd_tokens = tokenize(cmd)

        # 执行该命令并获取新的状态
        status = execute(cmd_tokens)

def main():
    shell_loop()

if __name__ == '__main__':
    main()