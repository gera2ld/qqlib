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
``` python
import qqlib
qq = qqlib.QQ(12345678, 'password')
qq.login()
qq.say_hi()

# QZone
from qqlib import qzone
qq = qzone.QZone(12345678, 'password')
qq.login()
qq.feed('发一条说说')
```

测试
---
``` sh
$ python -m test
$ python3 -m test
```
