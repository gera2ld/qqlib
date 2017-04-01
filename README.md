qqlib
===
[![PyPI](https://img.shields.io/pypi/v/qqlib.svg)]()

Python版QQ登录库，兼容Python2.x和Python3.x。

安装
---
``` sh
$ pip install qqlib
# or
$ pip install git+https://github.com/gera2ld/qqlib.git
```

快速开始
---
``` sh
$ python -m qqlib
```

高级用法
---
``` python
def login(qq):
    # 不考虑验证码的情况，直接登录
    qq.login()

import qqlib
qq = qqlib.QQ(12345678, 'password')
login(qq)
print('Hi, %s' % qq.nick)
```

登录时有可能出现需要验证码的情况，可以捕获到`qqlib.NeedVerifyCode`错误。这时`qq.need_verify`为`True`，需要获取验证码图片（`qq.verifier.fetch_image()`）进行处理，验证（`qq.verifier.verify(code)`）之后再继续登录。下面是支持输入验证码的`login`方法：
``` python
def login(qq):
    # 自动重试登录
    while True:
        try:
            if qq.need_verify:
                open('verify.jpg', 'wb').write(qq.verifier.fetch_image())
                print('验证码已保存到verify.jpg')
                # 输入验证码
                vcode = input('请输入验证码：')
                qq.verifier.verify(vcode)
            qq.login()
            break
        except qqlib.NeedVerifyCode as exc:
            if exc.message:
                print('Error:', exc.message)
```

QZone：
``` python
from qqlib import qzone
qq = qzone.QZone(12345678, 'password')
# 登录流程同上
login(qq)
qq.feed('发一条说说')
```

测试
---
``` sh
# Python 2
$ python -m unittest discover

# Python 3
$ python3 -m unittest
```
