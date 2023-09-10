from random import choice
from unittest import TestCase


def random_token(length=64):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join([choice(chars) for i in range(length)])

VALID_TOKEN         = random_token(64)    # 64 characters
INVALID_TOKEN_SHORT = random_token(63)    # 63 characters
INVALID_TOKEN_LONG  = random_token(65)    # 65 characters

class SilentTestCases(TestCase):
    def setUp(self):
        self.original_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        sys.stdout = self.original_stdout
