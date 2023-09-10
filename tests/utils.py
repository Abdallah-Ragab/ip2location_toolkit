from random import choice


def random_token(length=64):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join([choice(chars) for i in range(length)])

VALID_TOKEN         = random_token(64)    # 64 characters
INVALID_TOKEN_SHORT = random_token(63)    # 63 characters
INVALID_TOKEN_LONG  = random_token(65)    # 65 characters
