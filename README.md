QQLib for Python
===

Python版QQ登录库，兼容Python2.x和Python3.x。

安装
---
``` sh
$ pip install git+https://github.com/gera2ld/qqlib.git
```

使用方法
---
快速尝试一下可以执行如下命令：
``` sh
$ python -m qqlib
```

更高级的用法如下：
``` python
import qqlib
qq = qqlib.QQ(12345678, 'password')
try:
    qq.login()
except qqlib.NeedVerifyCode as e:
    # 需要验证码
    verifier = e.verifier
    open('verify.jpg', 'wb').write(verifier.image)
    print('验证码已保存到verify.jpg')
    # 输入验证码
    vcode = input('请输入验证码：')
    try:
        # 验证
        kw = verifier.verify(vcode)
    except qqlib.VerifyCodeError as e:
        print('验证码错误！')
        raise e
    else:
        # 继续登录
        qq.login()
print('Hi, %s' % qq.nick)

# QZone
from qqlib import qzone
qq = qzone.QZone(12345678, 'password')
# 先完成登录...
qq.feed('发一条说说')
```

测试
---
``` sh
$ python -m unittest
$ python3 -m unittest
```
