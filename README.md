QQLib for Python
===

Python版QQ登录库，兼容Python2.x和Python3.x。

安装
---
1. 安装依赖：
  ``` sh
  $ pip install -r requirements.txt
  ```

1. 安装qqlib：
  ``` sh
  $ python setup.py install
  ```
  或直接复制`qqlib`到合适的位置。

使用方法
---
``` python
import qqlib
qq = qqlib.QQ(12345678, 'password')
qq.login()
qq.sayHi()
```
