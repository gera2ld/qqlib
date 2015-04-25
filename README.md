QQLib for Python
===

基于webqq的Python版QQ登录库。
兼容Python2.x和Python3.x。

安装
---
第三方依赖：[rsa](https://pypi.python.org/pypi/rsa/)、[requests](https://pypi.python.org/pypi/requests/)。

``` sh
$ pip install rsa requests
$ python setup.py install
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
