QQLib for Python
===

Python版QQ登录库，兼容Python2.x和Python3.x。

安装
---
``` sh
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

登录时有可能出现需要验证码的情况，这时可以捕获`qqlib.NeedVerifyCode`错误并从中获取验证码图片（`exc.verifier.image`）进行处理，验证（`exc.verifier.verify(code)`）之后再继续登录。下面是支持输入验证码的`login`方法：
``` python
def login(qq):
    # 捕获验证码
    try:
        qq.login()
    except qqlib.NeedVerifyCode as e:
        # 需要验证码
        verifier = e.verifier
        open('verify.jpg', 'wb').write(verifier.image)
        print('验证码已保存到verify.jpg')
        # 输入验证码
        vcode = raw_input('请输入验证码：')
        try:
            # 验证
            kw = verifier.verify(vcode)
        except qqlib.VerifyCodeError as e:
            print('验证码错误！')
            raise e
        else:
            # 继续登录
            qq.login()
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
$ python -m unittest
$ python3 -m unittest
```
