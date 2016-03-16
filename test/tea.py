#!/usr/bin/env python
# coding=utf-8
from binascii import a2b_hex, b2a_hex
from qqlib import tea
from .base import show_start, show_result

KEY_1 = b'aaaabbbbccccdddd'
DATA_1 = b'abcdefgh'
ENC_1 = b'a557272c538d3e96'

def test_encipher():
    show_start('encipher')
    c = b2a_hex(tea.encipher(DATA_1, KEY_1))
    show_result(c == ENC_1)

def test_decipher():
    show_start('decipher')
    c = tea.decipher(a2b_hex(ENC_1), KEY_1)
    show_result(c == DATA_1)

KEY_2 = b2a_hex(b'b537a06cf3bcb33206237d7149c27bc3')
DATA_2 = b''
ENC_2 = b'b56137502728e2c74bb84c6d50d21973'

def test_encrypt():
    show_start('encrypt')
    e = b2a_hex(tea.encrypt(DATA_2, KEY_2))
    show_result(e == ENC_2)

def test_decrypt():
    show_start('decrypt')
    c = tea.decrypt(a2b_hex(ENC_2), KEY_2)
    show_result(c == DATA_2)

def test():
    test_encipher()
    test_decipher()
    test_encrypt()
    test_decrypt()
