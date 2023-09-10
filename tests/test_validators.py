from ip2location_toolkit.validators import path_validator, token_validator, db_code_validator, get_all_db_codes
from unittest import TestCase
import os, pathlib
from .utils import VALID_TOKEN, INVALID_TOKEN_SHORT, INVALID_TOKEN_LONG

class TestPathValidator(TestCase):
    def test_path_is_none_required(self):
        path = None
        with self.assertRaises(ValueError, msg='None path should raise ValueError if required=True'):
            path_validator(path)

    def test_path_is_none_not_required(self):
        path = None
        result = path_validator(path, required=False)
        self.assertEqual(result, path, msg='None path should return the same value if required=False')

    def test_path_is_not_str_convertible(self):
        path = 123 + 456j
        with self.assertRaises(ValueError, msg='Non string convertible path should raise ValueError'):
            path_validator(path)

    def test_path_is_str_convertible(self):
        path = pathlib.Path(os.path.abspath(__file__)).parent
        result = path_validator(path)
        self.assertEqual(result, path, msg='The path should be returned if it is string convertible')

    def test_path_empty_required(self):
        path = ''
        with self.assertRaises(ValueError, msg='Empty path should raise ValueError if required=True'):
            path_validator(path)

    def test_path_empty_not_required(self):
        path = ''
        result = path_validator(path, required=False)
        self.assertEqual(result, path, msg='Empty path should return the same value if required=False')

    def test_path_not_exists(self):
        path = "__test_path__"
        self.assertFalse(os.path.exists(path), msg='This path should not exist' + str(path))

        with self.assertRaises(ValueError, msg='Path that does not exist should raise ValueError'):
            path_validator(path)
        with self.assertRaises(ValueError, msg='Path that does not exist should raise ValueError'):
            path_validator(path, required=False)

    def test_valid_path(self):
        path = pathlib.Path(os.path.abspath(__file__)).parent
        self.assertTrue(os.path.exists(path), msg='Path of the directory of the current file should exist')
        result = path_validator(path)
        self.assertEqual(result, path, msg='The path should be returned if it exists and is not empty')
        result = path_validator(path, required=False)
        self.assertEqual(result, path, msg='The path should be returned if it exists and is not empty')

class TestTokenValidator(TestCase):
    def test_token_empty(self):
        token = ''
        with self.assertRaises(ValueError, msg='Valid token should raise ValueError if the token is empty'):
            token_validator(token)

    def test_token_length_less_than_64(self):
        token = INVALID_TOKEN_SHORT
        with self.assertRaises(ValueError, msg='Token length less than 64 should raise ValueError'):
            token_validator(token)

    def test_token_length_more_than_64(self):
        token = INVALID_TOKEN_LONG
        with self.assertRaises(ValueError, msg='Token length more than 64 should raise ValueError'):
            token_validator(token)

    def test_token_length_is_64(self):
        token = VALID_TOKEN
        result = token_validator(token)
        self.assertEqual(result, token, msg='The token should be returned if it is 64 characters long')

class TestDbCodeValidator(TestCase):
    def test_db_code_empty(self):
        db_code = ''
        with self.assertRaises(ValueError, msg='Valid db_code should raise ValueError if the db_code is empty'):
            db_code_validator(db_code)

    def test_db_code_not_in_all_db_codes(self):
        db_code = 'DB1'
        with self.assertRaises(ValueError, msg='Valid db_code should raise ValueError if the db_code is not in all_db_codes'):
            db_code_validator(db_code)

    def test_db_code_in_all_db_codes(self):
        db_code = get_all_db_codes()[0]
        result = db_code_validator(db_code)
        self.assertEqual(result, db_code, msg='The db_code should be returned if it is in all_db_codes')