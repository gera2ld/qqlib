QQLib for Python
===

基于webqq的Python版QQ登录库。

安装
---
``` sh
$ python3 setup.py install
```
或直接复制`qqlib`到合适的位置。

使用方法
---
``` python
import qqlib
qq=qqlib.QQ(12345678,'password')
qq.login()
qq.sayHi()
```
