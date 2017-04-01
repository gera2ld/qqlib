import getpass, sys, tempfile, os
from . import QQ, NeedVerifyCode

quser = input('QQ: ')
qpwd = getpass.getpass('Password: ')

qq = QQ(quser, qpwd)
while True:
    try:
        if qq.need_verify:
            fd, path = tempfile.mkstemp(suffix='.jpg')
            os.write(fd, qq.verifier.fetch_image())
            os.close(fd)
            print('Verify code is saved to:', path)
            vcode = input('Input verify code: ')
            os.remove(path)
            qq.verifier.verify(vcode)
        qq.login()
        break
    except NeedVerifyCode:
        exc = sys.exc_info()[1]
        if exc.message:
            print('Error:', exc.message)
        exc = None
print('Hi, %s' % qq.nick)
