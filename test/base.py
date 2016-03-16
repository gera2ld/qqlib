#!/usr/bin/env python
# coding=utf-8
import sys

def show_start(name):
    sys.stdout.write('Test %s: ' % name)

def show_result(res):
    sys.stdout.write('OK' if res else 'ERROR!')
    sys.stdout.write('\n')
