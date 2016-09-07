#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import shlex
from yash.builtins import *
from yash.constants import *

built_in_cmds = {}

def register_command(name, func):
    built_in_cmds[name] = func

def tokenize(string):
    return shlex.split(string)

def execute(cmd_tokens):
    cmd_name = cmd_tokens[0]
    cmd_args = cmd_tokens[1:]

    if cmd_name in built_in_cmds:
        return built_in_cmds[cmd_name](cmd_args)

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

def init():
    register_command('cd', cd)

def main():
    init()
    shell_loop()

if __name__ == '__main__':
    main()