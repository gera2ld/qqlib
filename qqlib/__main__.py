#!/usr/bin/env python
# coding=utf-8
import getpass
from . import QQ

quser = input('请输入QQ：')
qpwd = getpass.getpass('请输入密码：')

qq = QQ(quser, qpwd)
qq.login()
qq.say_hi()
