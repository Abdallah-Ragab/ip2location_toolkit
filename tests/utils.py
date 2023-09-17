from functools import partialmethod
from random import choice
from unittest import TestCase
import io, sys
from pathlib import Path
from tqdm import tqdm


def recursive_remove_dir(path: Path):
    """
    Recursively remove a directory and all its contents.
    @param path - the path to the directory to remove
    @return None
    """
    if isinstance(path, str):
        path = Path(path)

    if path.is_dir():
        for child in path.iterdir():
            recursive_remove_dir(child)
        path.rmdir()
    else:
        path.unlink()

def random_token(length=64):
    """
    Generate a random token of a specified length.
    @param length - the length of the token (default is 64)
    @return A random token string
    """
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join([choice(chars) for i in range(length)])

VALID_TOKEN         = random_token(64)    # 64 characters
INVALID_TOKEN_SHORT = random_token(63)    # 63 characters
INVALID_TOKEN_LONG  = random_token(65)    # 65 characters

class SilentTestCase(TestCase):
    """
    A test case class for testing code that produces silent output. It redirects the standard output to a string buffer during the test setup and restores it to the original standard output during the test teardown.
    This allows for testing code that does not produce any visible output.
    The `setUp` method saves the original standard output and replaces it with a string buffer.
    The `tearDown` method restores the original standard output.
    """
    def setUp(self):
        """
        Set up the test environment by redirecting the standard output to a string buffer.
        @return None
        """
        self.original_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        """
        Restore the original standard output stream.
        @param self - the current instance of the test case
        @return None
        """
        sys.stdout = self.original_stdout


class SilentTqdm(tqdm):
    def __init__(self, *args, **kwargs):
        kwargs['disable'] = True
        super().__init__(*args, **kwargs)
