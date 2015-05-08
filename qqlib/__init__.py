#!python
# coding=utf-8
'''
QQ Login module
Maintainer: Gerald <gera2ld@163.com>
Last change: 2015 Apr 20
'''
import os, hashlib, re, tempfile, binascii, base64
import rsa, requests
from . import tea
__all__ = ['QQ', 'LogInError']

class LogInError(Exception): pass

class QQ:
	'''
	>>> qq = QQ(12345678, 'password')
	>>> qq.login()
	>>> qq.sayHi()
	'''
	appid=501004106
	action='0-21-1083992'
	proxyurl='http://w.qq.com/proxy.html'
	checkurl='https://ssl.ptlogin2.qq.com/check'
	imgurl='http://captcha.qq.com/getimage'
	loginurl='https://ssl.ptlogin2.qq.com/login'

	def __init__(self, user, pwd):
		self.user = user
		self.pwd = pwd
		self.session = requests.Session()

	def fetch(self, url, data=None, **kw):
		if data is None:
			func = self.session.get
		else:
			kw['data'] = data
			func = self.session.post
		return func(url, **kw)

	def login(self):
		g = self.fetch(self.checkurl, params = {
			'pt_tea': 1,
			'uin': self.user,
			'appid': self.appid,
			'js_ver': 10120,
			'js_type': 0,
			'u1': self.proxyurl,
		}).text
		v = re.findall('\'(.*?)\'', g)
		vcode = v[1]
		uin = v[2]
		if v[0] == '1':	# verify code needed
			vcode = self.getVerifyCode(vcode)
		g = self.fetch(self.loginurl, params = {
			'u': self.user,
			'p': self.pwdencode(vcode, uin, self.pwd),
			'verifycode': vcode,
			'webqq_type': 10,
			'remember_uin': 1,
			'login2qq': 1,
			'aid': self.appid,
			'u1': self.proxyurl,
			'h': 1,
			'ptredirect': 0,
			'ptlang': 2052,
			'daid': 164,
			'from_ui': 1,
			'fp': 'loginerroralert',
			'action': self.action,
			'mibao_css': 'm_webqq',
			't': 1,
			'g': 1,
			'js_type': 0,
			'js_ver': 10120,
			'pt_randsalt': 0,
			'pt_vcode_v1': 0,
			'pt_verifysession_v1': self.session.cookies['ptvfsession'],
		}).text
		r = re.findall('\'(.*?)\'', g)
		if r[0] != '0':
			raise LogInError(r[4])
		self.nick = r[5]

	def fromhex(self, s):
		# Python 3: bytes.fromhex
		return bytes(bytearray.fromhex(s))

	pubKey=rsa.PublicKey(int(
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

	def getVerifyCode(self, vcode):
		r = self.fetch(self.imgurl, params = {
			'r':0,
			'appid':self.appid,
			'uin':self.user,
			'vc_type':vcode,
		})
		tmp = tempfile.mkstemp(suffix = '.jpg')
		os.write(tmp[0], r.content)
		os.close(tmp[0])
		os.startfile(tmp[1])
		vcode = input('Verify code: ')
		os.remove(tmp[1])
		return vcode

	def sayHi(self):
		print('Hi, %s!' % getattr(self, 'nick') or self.user)
