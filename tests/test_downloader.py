from unittest.mock import MagicMock, patch
from unittest import TestCase
from ip2location_toolkit.downloader.download import download_file, download_database, unzip_db, download_extract_db, get_dir_or_create, get_tmp_dir, get_downloaded_zip_path
from ip2location_toolkit.downloader.cli import db_code_prompt, token_prompt, output_prompt
from ip2location_toolkit.exceptions import DataBaseNotFound, DownloadLimitExceeded, DownloadPermissionDenied
import os, io, sys, zipfile

from .utils import VALID_TOKEN, INVALID_TOKEN_SHORT, INVALID_TOKEN_LONG
from .utils import SilentTestCases

mocked_404_response = MagicMock(status_code=404)
mocked_limit_exceeded_response = MagicMock(status_code=200, text='THIS FILE CAN ONLY BE DOWNLOADED')
mocked_permission_response = MagicMock(status_code=200, text='NO PERMISSION')

class TestGetDownloadedZipPath(TestCase):
    def test_get_downloaded_zip_path(self):
        result = get_downloaded_zip_path('DB1LITEBIN')
        self.assertEqual(result, os.path.join(get_tmp_dir(), 'DB1LITEBIN.zip'), msg="The function should return the path to the tmp directory + the file code + .zip.")

class TestGetDirOrCreate(TestCase):
    def test_existing_dir(self):
        test_dir = 'test_dir'
        os.mkdir(test_dir)
        result = get_dir_or_create(test_dir)
        self.assertEqual(result, test_dir, msg="The function should return the path to the test directory.")
        os.rmdir(test_dir)

    def test_new_dir(self):
        test_dir = 'test_dir'
        self.assertFalse(os.path.exists(test_dir), msg="The test directory should not exist.")
        result = get_dir_or_create(test_dir)
        self.assertTrue(os.path.exists(test_dir), msg="The test directory should exist.")
        self.assertEqual(result, test_dir)
        os.rmdir(test_dir)

class TestGetTMPDir(TestCase):
    def test_tmp_dir(self):
        result = get_tmp_dir()
        self.assertTrue(os.path.exists(result), msg="The tmp directory should exist.")
        self.assertEqual(result, os.path.join(os.getcwd(), 'tmp'), msg="The function should return the path to the tmp directory. The path should be the same as the current working directory + tmp.")

class TestDownloadFile(SilentTestCases):
    @patch('ip2location_toolkit.downloader.download.requests.get', return_value=mocked_404_response)
    def test_404_response(self, mocker):
        with self.assertRaises(DataBaseNotFound, msg="Expected DataBaseNotFound exception to be raised"):
            download_file('https://www.ip2location.com/download?token=123&file=DB1LITEBIN', 'test.zip')

    @patch('ip2location_toolkit.downloader.download.requests.get', return_value=mocked_limit_exceeded_response)
    def test_limit_exceeded_response(self, mocker):
        with self.assertRaises(DownloadLimitExceeded, msg="Expected DownloadLimitExceeded exception to be raised"):
            download_file('https://www.ip2location.com/download?token=123&file=DB1LITEBIN', 'test.zip')


    @patch('ip2location_toolkit.downloader.download.requests.get', return_value=mocked_permission_response)
    def test_permission_response(self, mocker):
        with self.assertRaises(DownloadPermissionDenied, msg="Expected DownloadPermissionDenied exception to be raised"):
            download_file('https://www.ip2location.com/download?token=123&file=DB1LITEBIN', 'test.zip')

    @patch('ip2location_toolkit.downloader.download.requests.get', return_value=MagicMock(status_code=200, text='test'))
    def test_download_file(self, mocker):
        file = download_file('https://www.ip2location.com/download?token=123&file=DB1LITEBIN', 'test.zip')
        self.assertEqual(file, 'test.zip', msg="The function should return the path to the downloaded zip file.")
        self.assertTrue(os.path.exists(file), msg="The downloaded zip file should exist.")
        os.remove(file)

class TestDownloadDatabase(SilentTestCases):

    def test_invalid_token(self):
        self.assertIsNone(download_database('DB1LITEBIN', INVALID_TOKEN_LONG), msg="Expected None to be returned for invalid token.")

    @patch('ip2location_toolkit.downloader.download.download_file', return_value='test.zip')
    def test_download_database(self, mocker):
        file = download_database('DB1LITEBIN', VALID_TOKEN)
        self.assertEqual(file, 'test.zip', msg="The function should return the path to the downloaded zip file.")

    @patch('ip2location_toolkit.downloader.download.download_file', return_value=None, side_effect=DataBaseNotFound)
    def test_download_file_failed(self, mocker):
        file = download_database('DB1LITEBIN', VALID_TOKEN)
        self.assertIsNone(file, msg="The function should return None if the download_file function failed.")


class TestUnzipDB(SilentTestCases):
    def create_zip_file(self):

        self.zipfile_name = self.file_name.split('.')[0] + '.zip'
        self.zipfile_path = os.path.join(os.getcwd(), self.zipfile_name)

        # create a file and zip it
        with open(self.file_name, 'w') as f:
            f.write('This is a test file.')

        with zipfile.ZipFile(self.zipfile_name, 'w') as zip_file:
            zip_file.write(self.file_name)

        self.assertTrue(os.path.exists(self.zipfile_name), msg="The zip file should exist.")

    def setUp(self):
        self.file_name = 'test_file.bin'
        self.output_dir = 'unzipped'
        self.create_zip_file()
        return super().setUp()

    def tearDown(self):
        if os.path.exists(getattr(self, 'file_name', '')):
            os.remove(self.file_name)
        if os.path.exists(getattr(self, 'zipfile_name', '')):
            os.remove(self.zipfile_name)
        if os.path.exists(getattr(self, 'output_file_path', '')):
            os.remove(self.output_file_path)
        if os.path.exists(getattr(self, 'output_dir', '')):
            os.rmdir(self.output_dir)

    def test_unzip_db(self):
        self.output_file_path = unzip_db('test_file.zip', self.output_dir)
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, self. file_name)), msg="The unzipped file should exist.")

    @patch('ip2location_toolkit.downloader.download.ZipFile.extract', side_effect=zipfile.BadZipFile)
    def test_failed_unzip(self, mocker):
        with self.assertRaises(zipfile.BadZipFile, msg="Expected BadZipFile exception to be raised"):
            unzip_db('test_file.zip', self.output_dir)

class TestDownloadExtractDB(TestCase):
    def test_invalid_token(self):
        result = download_extract_db('DB1LITEBIN', INVALID_TOKEN_LONG)
        self.assertIsNone(result, msg="Expected ValueError Exception to be raised when token is invalid")

    def test_invalid_db_code(self):
        result = download_extract_db('DB1LITEBINXX', VALID_TOKEN)
        self.assertIsNone(result, msg="Expected ValueError Exception to be raised when db_code is invalid")

    def test_invalid_path(self):
        result = download_extract_db('DB1LITEBIN', VALID_TOKEN, 'invalid_path')
        self.assertIsNone(result, msg="Expected ValueError Exception to be raised when path is invalid")

    @patch('ip2location_toolkit.downloader.download.download_database', return_value='test.zip')
    @patch('ip2location_toolkit.downloader.download.unzip_db', return_value='hjk')
    def test_download_extract_db(self, unzip_db_mock, download_database_mock):
        file = download_extract_db('DB1LITEBIN', VALID_TOKEN)
        print(file)
        self.assertEqual(file, 'hjk', msg="The function should return the path to the downloaded zip file.")

    @patch('ip2location_toolkit.downloader.download.download_database', return_value=None)
    def test_failed_download_database(self, download_database_mock):
        result = download_extract_db('DB1LITEBIN', VALID_TOKEN)
        self.assertIsNone(result, msg="The function should return None if the download_database function failed.")