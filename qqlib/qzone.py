'''
QZone module
'''

from . import QQ
from . import hieroglyphy

class QZone(QQ):
    url_success = 'http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone'
    url_feed = 'http://taotao.qzone.qq.com/cgi-bin/emotion_cgi_publish_v6'
    url_home = 'https://user.qzone.qq.com/'

    def g_tk(self):
        h = 5381
        cookies = self.session.cookies
        s = cookies.get('p_skey') or cookies.get('skey') or ''
        for c in s:
            h += (h << 5) + ord(c)
        return h & 0x7fffffff

    def _qzonetoken(self, res, start_str, end_str=';'):
        i = res.find(start_str)
        j = res.find(';', i)
        assert i > 0, 'qzonetoken not found!'
        raw = res[i + len(start_str) : j]
        return hieroglyphy.decode(raw)

    def qzonetoken(self):
        self.fetch(self.url_success)
        res = self.fetch(self.url_home + str(self.user), headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
        }).text
        return self._qzonetoken(res, 'window.g_qzonetoken = (function(){ try{return ')

    def _feed(self, data):
        return self.fetch(self.url_feed, params={
            'g_tk': self.g_tk(),
            'qzonetoken': self.qzonetoken(),
        }, data = {
            'syn_tweet_verson'    : 1,
            'paramstr'            : 1,
            'pic_template'        : '',
            'richtype'            : '',
            'richval'             : '',
            'special_url'         : '',
            'subrichtype'         : '',
            'who'                 : 1,
            'con'                 : data,
            'feedversion'         : 1,
            'ver'                 : 1,
            'ugc_right'           : 1,
            'to_tweet'            : 0,
            'to_sign'             : 0,
            'hostuin'             : self.user,
            'code_version'        : 1,
            'format'              : 'fs'
        })

    def feed(self, data):
        res = self._feed(data)
        res.raise_for_status()

class MQZone(QZone):
    url_success = 'https://h5.qzone.qq.com/mqzone/index'
    url_feed = 'https://mobile.qzone.qq.com/mood/publish_mood'

    def qzonetoken(self):
        res = self.fetch(self.url_success).text
        return self._qzonetoken(res, 'window.shine0callback = (function(){ try{return ')

    def _feed(self, data):
        return self.fetch(self.url_feed, params={
            'g_tk': self.g_tk(),
            'qzonetoken': self.qzonetoken(),
        }, data = {
            'opr_type': 'publish_shuoshuo',
            'res_uin': self.user,
            'content': data,
            'richval': '',
            'lat': 0,
            'lon': 0,
            'lbsid': '',
            'issyncweibo': 0,
            'format': 'json',
        })
