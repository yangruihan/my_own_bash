#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from yash.constants import *

def cd(args):
    os.chdir(args[0])
    return SHELL_STATUS_RUN