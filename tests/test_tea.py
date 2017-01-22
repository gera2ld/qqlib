import unittest
from binascii import a2b_hex, b2a_hex
from qqlib import tea

KEY_1 = b'aaaabbbbccccdddd'
DATA_1 = b'abcdefgh'
ENC_1 = b'a557272c538d3e96'
KEY_2 = b2a_hex(b'b537a06cf3bcb33206237d7149c27bc3')
DATA_2 = b''
ENC_2 = b'b56137502728e2c74bb84c6d50d21973'

class TestTEA(unittest.TestCase):
    def test_encipher(self):
        c = b2a_hex(tea.encipher(DATA_1, KEY_1))
        self.assertEqual(c, ENC_1)

    def test_decipher(self):
        c = tea.decipher(a2b_hex(ENC_1), KEY_1)
        self.assertEqual(c, DATA_1)

    def test_encrypt(self):
        e = b2a_hex(tea.encrypt(DATA_2, KEY_2))
        self.assertEqual(e, ENC_2)

    def test_decrypt(self):
        c = tea.decrypt(a2b_hex(ENC_2), KEY_2)
        self.assertEqual(c, DATA_2)
