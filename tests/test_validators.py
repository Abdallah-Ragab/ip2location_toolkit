from ip2location_toolkit.validators import path_validator, token_validator, db_code_validator
from unittest import TestCase
import os, pathlib


class TestPathValidator(TestCase):
    def test_path_required_empty(self):
        path = ''
        with self.assertRaises(ValueError, 'Empty path should raise ValueError if required=True'):
            path_validator(path)

    def test_path_not_required_empty(self):
        path = ''
        result = path_validator(path, required=False)
        self.assertEqual(result, path, 'Empty path should return the same value if required=False')

    def test_path_not_empty_exists(self):
        path = pathlib.Path(os.path.abspath(__file__)).parent
        self.assertTrue(os.path.exists(path), 'Path of the directory of the current file should exist')
        result = path_validator(path)
        self.assertEqual(result, path, 'The path should be returned if it exists and is not empty')
        result = path_validator(path, required=False)
        self.assertEqual(result, path, 'The path should be returned if it exists and is not empty')

    def test_path_not_empty_not_exists(self):
        path = '__test_path__'
        self.assertFalse(os.path.exists(path))
        with self.assertRaises(ValueError, 'Path that does not exist should raise ValueError'):
            path_validator(path)
        with self.assertRaises(ValueError, 'Path that does not exist should raise ValueError'):
            path_validator(path, required=False)


class TestTokenValidator(TestCase):
    def test_token_empty(self):
        token = ''
        with self.assertRaises(ValueError, 'The token '):
            token_validator(token)

    def test_token_length_less_than_16(self):
        token = '123456789012345'
        with self.assertRaises(ValueError):
            token_validator(token)

    def test_token_length_more_than_16(self):
        token = '12345678901234567'
        with self.assertRaises(ValueError):
            token_validator(token)

    def test_token_length_is_16(self):
        token = '1234567890123456'
        result = token_validator(token)
        self.assertEqual(result, token, 'The token should be returned if it is 16 characters long')