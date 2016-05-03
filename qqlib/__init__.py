#!/usr/bin/env python
# coding=utf-8

'''
QQ Login module
Licensed to MIT
'''

import os, hashlib, re, tempfile, binascii, base64
import rsa, requests
from . import tea
__all__ = ['QQ', 'LogInError']

class LogInError(Exception): pass

class QQ:
    appid = 549000912
    action = '4-22-1450611437613'
    url_success = 'http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone'
    url_check = 'http://check.ptlogin2.qq.com/check'
    url_image = 'http://captcha.qq.com/getimage'
    url_login = 'http://ptlogin2.qq.com/login'
    url_xlogin = 'http://xui.ptlogin2.qq.com/cgi-bin/xlogin'

    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.nick = None
        self.session = requests.Session()
        self.xlogin()

    def fetch(self, url, data=None, **kw):
        if data is None:
            func = self.session.get
        else:
            kw['data'] = data
            func = self.session.post
        return func(url, **kw)

    def xlogin(self):
        '''
        Get a log-in signature in cookies.
        '''
        self.fetch(self.url_xlogin, params = {
            'proxy_url': 'http://qzs.qq.com/qzone/v6/portal/proxy.html',
            'daid': 5,
            'no_verifyimg': 1,
            'appid': self.appid,
            's_url': self.url_success,
        })
        # print('login_sig:', self.session.cookies['pt_login_sig'])

    def login(self):
        '''
        Check for verify code and log in.
        '''
        login_sig = self.session.cookies['pt_login_sig']
        g = self.fetch(self.url_check, params = {
            'pt_tea': 1,
            'uin': self.user,
            'appid': self.appid,
            'js_ver': 10143,
            'js_type': 1,
            'u1': self.url_success,
            'login_sig': login_sig,
        }).text
        v = re.findall('\'(.*?)\'', g)
        vcode = v[1]
        uin = v[2]
        ptvfsession = v[3]
        if v[0] == '1': # verify code needed
            vcode = self.get_verify_code(vcode)
        # `ptvfsession` may change
        ptvfsession = self.session.cookies.get('ptvfsession', ptvfsession)
        g = self.fetch(self.url_login, params = {
            'u': self.user,
            'verifycode': vcode,
            'pt_vcode_v1': 0,
            'pt_verifysession_v1': ptvfsession,
            'p': self.pwdencode(vcode, uin, self.pwd),
            'pt_randsalt': 0,
            'u1': self.url_success,
            'ptredirect': 0,
            'h': 1,
            't': 1,
            'g': 1,
            'from_ui': 1,
            'ptlang': 2052,
            'action': self.action,
            'js_ver': 10143,
            'js_type': 1,
            'aid': self.appid,
            'daid': 5,
            'login_sig': login_sig,
        }).text
        r = re.findall('\'(.*?)\'', g)
        if r[0] != '0':
            raise LogInError(r[4])
        self.nick = r[5]
        self.fetch(r[2])

    def fromhex(self, s):
        # Python 3: bytes.fromhex
        return bytes(bytearray.fromhex(s))

    pubKey = rsa.PublicKey(int(
        'F20CE00BAE5361F8FA3AE9CEFA495362'
        'FF7DA1BA628F64A347F0A8C012BF0B25'
        '4A30CD92ABFFE7A6EE0DC424CB6166F8'
        '819EFA5BCCB20EDFB4AD02E412CCF579'
        'B1CA711D55B8B0B3AEB60153D5E0693A'
        '2A86F3167D7847A0CB8B00004716A909'
        '5D9BADC977CBB804DBDCBA6029A97108'
        '69A453F27DFDDF83C016D928B3CBF4C7',
        16
    ), 3)
    def pwdencode(self, vcode, uin, pwd):
        '''
        Encode password with tea.
        '''
        # uin is the bytes of QQ number stored in unsigned long (8 bytes)
        salt = uin.replace(r'\x', '')
        h1 = hashlib.md5(pwd.encode()).digest()
        s2 = hashlib.md5(h1 + self.fromhex(salt)).hexdigest().upper()
        rsaH1 = binascii.b2a_hex(rsa.encrypt(h1, self.pubKey)).decode()
        rsaH1Len = hex(len(rsaH1) // 2)[2:]
        hexVcode = binascii.b2a_hex(vcode.upper().encode()).decode()
        vcodeLen = hex(len(hexVcode) // 2)[2:]
        l = len(vcodeLen)
        if l < 4:
            vcodeLen = '0' * (4 - l) + vcodeLen
        l = len(rsaH1Len)
        if l < 4:
            rsaH1Len = '0' * (4 - l) + rsaH1Len
        pwd1 = rsaH1Len + rsaH1 + salt + vcodeLen + hexVcode
        saltPwd = base64.b64encode(
            tea.encrypt(self.fromhex(pwd1), self.fromhex(s2))
        ).decode().replace('/', '-').replace('+', '*').replace('=', '_')
        return saltPwd

    def get_verify_code(self, vcode):
        '''
        Get the verify code image and ask use for a verification.
        '''
        r = self.fetch(self.url_image, params = {
            'r': 0,
            'appid': self.appid,
            'uin': self.user,
            'vc_type': vcode,
        })
        tmp = tempfile.mkstemp(suffix = '.jpg')
        os.write(tmp[0], r.content)
        os.close(tmp[0])
        os.startfile(tmp[1])
        vcode = input('Verify code: ')
        os.remove(tmp[1])
        return vcode

    def say_hi(self):
        print('Hi, %s!' % (self.nick or self.user))
