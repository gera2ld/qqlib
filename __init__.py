#!python
# coding=utf-8
import os,hashlib,re,tempfile,fetcher,rsa,binascii,base64
from . import tea
__all__ = ['QQ', 'LogInError']

class LogInError(Exception): pass

class QQ(fetcher.Fetcher):
	appid=501004106
	action='0-21-1083992'
	proxyurl='http://w.qq.com/proxy.html'
	checkurl='https://ssl.ptlogin2.qq.com/check'
	imgurl='http://captcha.qq.com/getimage'
	loginurl='https://ssl.ptlogin2.qq.com/login'
	def __init__(self,user,pwd):
		super().__init__()
		self.user=user
		self.pwd=pwd
	def login(self):
		g=self.fetch(self.checkurl, params={
			'pt_tea': 1,
			'uin': self.user,
			'appid': self.appid,
			'js_ver': 10120,
			'js_type': 0,
			'u1': self.proxyurl,
		}).text()
		v=re.findall('\'(.*?)\'',g)
		vcode=v[1]
		uin=v[2]
		if v[0]=='1':	# verify code needed
			vcode=self.getVerifyCode(vcode)
		g=self.fetch(self.loginurl,params={
			'u':self.user,
			'p':self.pwdencode(vcode, uin, self.pwd),
			'verifycode':vcode,
			'webqq_type':10,
			'remember_uin':1,
			'login2qq':1,
			'aid':self.appid,
			'u1':self.proxyurl,
			'h':1,
			'ptredirect':0,
			'ptlang':2052,
			'daid':164,
			'from_ui':1,
			'fp':'loginerroralert',
			'action':self.action,
			'mibao_css':'m_webqq',
			't':1,
			'g':1,
			'js_type':0,
			'js_ver':10120,
			'pt_randsalt':0,
			'pt_vcode_v1':0,
			'pt_verifysession_v1':self.getCookie('ptvfsession'),
		}).text()
		r=re.findall('\'(.*?)\'',g)
		if r[0]!='0': raise LogInError(r[4])
		self.nick=r[5]
	def pwdencode(self, vcode, uin, pwd):
		# uin is the bytes of QQ number stored in 8B
		salt=uin.replace(r'\x','')
		if isinstance(pwd,str):
			h1=hashlib.md5(pwd.encode()).digest()
		else:
			h1=pwd
		s2=hashlib.md5(h1+bytes.fromhex(salt)).hexdigest().upper()
		pub=rsa.PublicKey(int(
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
		rsaH1=binascii.b2a_hex(rsa.encrypt(h1,pub)).decode()
		rsaH1Len=hex(len(rsaH1)//2)[2:]
		hexVcode=binascii.b2a_hex(vcode.upper().encode()).decode()
		vcodeLen=hex(len(hexVcode)//2)[2:]
		l=len(vcodeLen)
		if l<4:
			vcodeLen='0'*(4-l)+vcodeLen
		l=len(rsaH1Len)
		if l<4:
			rsaH1Len='0'*(4-l)+rsaH1Len
		pwd1=rsaH1Len+rsaH1+salt+vcodeLen+hexVcode
		saltPwd=base64.b64encode(tea.encrypt(bytes.fromhex(pwd1),bytes.fromhex(s2))).decode().replace('/','-').replace('+','*').replace('=','_')
		return saltPwd
	def getVerifyCode(self,vcode):
		r=self.fetch(self.imgurl,
				params={'r':0,'appid':self.appid,
					'uin':self.user,'vc_type':vcode})
		tmp=tempfile.mkstemp(suffix='.jpg')
		os.write(tmp[0],r.raw())
		os.close(tmp[0])
		os.startfile(tmp[1])
		vcode=input('Verify code: ')
		os.remove(tmp[1])
		return vcode
	def sayHi(self):
		print('Hi, %s!' % getattr(self,'nick') or self.user)

if __name__=='__main__':
	q=QQ('12345678','password')
	q.login()
	q.sayHi()
