
from unittest.mock import MagicMock, patch
from unittest import TestCase
from ip2location_toolkit.downloader.download import download_file
from ip2location_toolkit.downloader.download import get_dir_or_create, get_tmp_dir, get_downloaded_zip_path
from ip2location_toolkit.exceptions import DataBaseNotFound, DownloadLimitExceeded, DownloadPermissionDenied
import os, io, sys

mocked_404_response = MagicMock(status_code=404)
mocked_limit_exceeded_response = MagicMock(status_code=200, text='THIS FILE CAN ONLY BE DOWNLOADED')
mocked_permission_response = MagicMock(status_code=200, text='NO PERMISSION')


class SilentTestCases(TestCase):
    def setUp(self):
        self.original_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        sys.stdout = self.original_stdout

class TestDownloadFile(SilentTestCases):
    @patch('ip2location_toolkit.downloader.download.requests.get', return_value=mocked_404_response)
    def test_404_response(self, mocker):
        with self.assertRaises(DataBaseNotFound):
            download_file('https://www.ip2location.com/download?token=123&file=DB1LITEBIN', 'test.zip')

    @patch('ip2location_toolkit.downloader.download.requests.get', return_value=mocked_limit_exceeded_response)
    def test_limit_exceeded_response(self, mocker):
        with self.assertRaises(DownloadLimitExceeded):
            download_file('https://www.ip2location.com/download?token=123&file=DB1LITEBIN', 'test.zip')


    @patch('ip2location_toolkit.downloader.download.requests.get', return_value=mocked_permission_response)
    def test_permission_response(self, mocker):
        with self.assertRaises(DownloadPermissionDenied):
            download_file('https://www.ip2location.com/download?token=123&file=DB1LITEBIN', 'test.zip')

class TestGetDownloadedZipPath(TestCase):
    def test_get_downloaded_zip_path(self):
        result = get_downloaded_zip_path('DB1LITEBIN')
        self.assertEqual(result, os.path.join(get_tmp_dir(), 'DB1LITEBIN.zip'), 'The function should return the path to the tmp directory + the file code + .zip.')

class TestGetDirOrCreate(TestCase):
    def test_existing_dir(self):
        test_dir = 'test_dir'
        os.mkdir(test_dir)
        result = get_dir_or_create(test_dir)
        self.assertEqual(result, test_dir, 'The function should return the path to the test directory.')
        os.rmdir(test_dir)

    def test_new_dir(self):
        test_dir = 'test_dir'
        self.assertFalse(os.path.exists(test_dir), 'The test directory should not exist.')
        result = get_dir_or_create(test_dir)
        self.assertTrue(os.path.exists(test_dir), 'The test directory should exist.')
        self.assertEqual(result, test_dir)
        os.rmdir(test_dir)

class TestGetTMPDir(TestCase):
    def test_tmp_dir(self):
        result = get_tmp_dir()
        self.assertTrue(os.path.exists(result), 'The tmp directory should exist.')
        self.assertEqual(result, os.path.join(os.getcwd(), 'tmp'), 'The function should return the path to the tmp directory. The path should be the same as the current working directory + tmp.')
