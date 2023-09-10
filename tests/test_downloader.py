from unittest.mock import MagicMock, patch
from unittest import TestCase
from ip2location_toolkit.downloader.download import download_file, download_database, unzip_db, download_extract_db
from ip2location_toolkit.downloader.download import get_dir_or_create, get_tmp_dir, get_downloaded_zip_path
from ip2location_toolkit.exceptions import DataBaseNotFound, DownloadLimitExceeded, DownloadPermissionDenied
import os, io, sys

from utils import VALID_TOKEN, INVALID_TOKEN_SHORT, INVALID_TOKEN_LONG


mocked_404_response = MagicMock(status_code=404)
mocked_limit_exceeded_response = MagicMock(status_code=200, text='THIS FILE CAN ONLY BE DOWNLOADED')
mocked_permission_response = MagicMock(status_code=200, text='NO PERMISSION')


class SilentTestCases(TestCase):
    def setUp(self):
        self.original_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        sys.stdout = self.original_stdout

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
        self.assertIsNone(download_database('DB1LITEBIN', '15154454'), msg="Expected None to be returned for invalid token.")

    @patch('ip2location_toolkit.downloader.download.download_file', return_value='test.zip')
    def test_download_database(self, mocker):
        file = download_database('DB1LITEBIN', VALID_TOKEN)
        self.assertEqual(file, 'test.zip', msg="The function should return the path to the downloaded zip file.")

    @patch('ip2location_toolkit.downloader.download.download_file', return_value=None, side_effect=DataBaseNotFound)
    def test_download_file_failed(self, mocker):
        file = download_database('DB1LITEBIN', VALID_TOKEN)
        self.assertIsNone(file, msg="The function should return None if the download_file function failed.")
