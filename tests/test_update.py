from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
from .utils import SilentTestCase, VALID_TOKEN
from ip2location_toolkit.downloader.update import version_to_date, get_db_version, new_version_available, get_db_header, update_db
import datetime, os

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestVersionToDate(TestCase):
    def test_version_to_date(self):
        version = "21.12.31"
        expected_date = datetime.date(2021, 12, 31)
        assert version_to_date(version) == expected_date

    def test_version_to_date_invalid_version_format_1(self):
        version = "21.12"
        with self.assertRaises(ValueError):
            version_to_date(version)
    def test_version_to_date_invalid_version_format_2(self):
        version = "xx.xx.xx"
        with self.assertRaises(ValueError):
            version_to_date(version)

class TestGetDBHeader(TestCase):
    @patch('ip2location_toolkit.downloader.update.path_validator', side_effect=ValueError)
    def test_invalid_file_path(self, mock_path_validator):
        filepath = "test/path/db.bin"
        with self.assertRaises(ValueError, msg="get_db_header() should raise ValueError if the file path is invalid"):
            get_db_header(filepath)

    @patch('ip2location_toolkit.downloader.update.path_validator')
    def test_valid_bin_file(self, mock_path_validator):
        path = TESTS_DIR + "/BINS/22-12-1-VALID.BIN"
        mock_path_validator.return_value = path
        with open(path, 'rb') as file:
            content = file.read()
        self.assertEqual(get_db_header(path), content[:30], "get_db_header() should return the first 30 bytes of the file")

    @patch('ip2location_toolkit.downloader.update.path_validator')
    def test_invalid_content_length(self, mock_path_validator):
        path = TESTS_DIR + "/BINS/29-BIT-INVALID.BIN"
        mock_path_validator.return_value = path
        with self.assertRaises(ValueError, msg="get_db_header() should raise ValueError if the file content is less than 30 bytes"):
            get_db_header(path)

    @patch('ip2location_toolkit.downloader.update.open', side_effect=IOError)
    @patch('ip2location_toolkit.downloader.update.path_validator')
    def test_error_reading_file(self, mock_path_validator, mock_open):
        path = TESTS_DIR + "/BINS/22-12-1-VALID.BIN"
        mock_path_validator.return_value = path
        with self.assertRaises(ValueError, msg="get_db_header() should raise ValueError if there is an error reading the file"):
            get_db_header(path)

class TestGetDBVersion(TestCase):
    @patch('ip2location_toolkit.downloader.update.get_db_header')
    def test_valid_version_22_12_1(self, mock_get_db_header):
        path = TESTS_DIR + "/BINS/22-12-1-VALID.BIN"
        with open(path, 'rb') as file:
            content = file.read()
        mock_get_db_header.return_value = content
        self.assertEqual(get_db_version(path), "22.12.1", "get_db_version() should return the correct version number (22.12.1)")

    @patch('ip2location_toolkit.downloader.update.get_db_header')
    def test_valid_version_23_5_1(self, mock_get_db_header):
        path = TESTS_DIR + "/BINS/23-5-1-VALID.BIN"
        with open(path, 'rb') as file:
            content = file.read()
        mock_get_db_header.return_value = content
        self.assertEqual(get_db_version(path), "23.5.1", "get_db_version() should return the correct version number (23.5.1)")

    @patch('ip2location_toolkit.downloader.update.get_db_header')
    def test_valid_version_23_9_1(self, mock_get_db_header):
        path = TESTS_DIR + "/BINS/23-9-1-VALID.BIN"
        with open(path, 'rb') as file:
            content = file.read()
        mock_get_db_header.return_value = content
        self.assertEqual(get_db_version(path), "23.9.1", "get_db_version() should return the correct version number (23.9.1)")

class TestNewVersionAvailable(TestCase):

    @patch('ip2location_toolkit.downloader.update.get_db_version')
    @patch('ip2location_toolkit.downloader.update.version_to_date')
    @patch('ip2location_toolkit.downloader.update.datetime', wraps=datetime)
    def test_new_version_available_earlier_month(self, mock_datetime, mock_version_to_date, mock_get_db_version):
        mock_get_db_version.return_value = "22.12.1"
        mock_version_to_date.return_value = datetime.date(2021, 12, 1)
        mock_datetime.date.today.return_value = datetime.date(2023, 9, 16)
        self.assertTrue(new_version_available("test/path/db.bin"), "new_version_available() should return True if the current date is later than the version date by a month or more")

    @patch('ip2location_toolkit.downloader.update.get_db_version')
    @patch('ip2location_toolkit.downloader.update.version_to_date')
    @patch('ip2location_toolkit.downloader.update.datetime', wraps=datetime)
    def test_new_version_available_same_month(self, mock_datetime, mock_version_to_date, mock_get_db_version):
        mock_get_db_version.return_value = "22.12.1"
        mock_version_to_date.return_value = datetime.date(2021, 12, 1)
        mock_datetime.date.today.return_value = datetime.date(2021, 12, 30)
        self.assertFalse(new_version_available("test/path/db.bin"), "new_version_available() should return False if the current date is earlier than the version date by less than a month")

    @patch('ip2location_toolkit.downloader.update.get_db_version')
    @patch('ip2location_toolkit.downloader.update.version_to_date')
    @patch('ip2location_toolkit.downloader.update.datetime', wraps=datetime)
    def test_new_version_available_later_month(self, mock_datetime, mock_version_to_date, mock_get_db_version):
        mock_datetime.date.today.return_value = datetime.date(2021, 11, 1)
        mock_get_db_version.return_value = "22.12.1"
        mock_version_to_date.return_value = datetime.date(2022, 12, 1)
        self.assertFalse(new_version_available("test/path/db.bin"), "new_version_available() should return False if the current date is earlier than the version date")

class TestUpdateDB(SilentTestCase):
    @patch('ip2location_toolkit.downloader.update.path_validator')
    def test_invalid_bin_filepath(self, mock_path_validator):
        filepath = "test/path/db.csv"
        mock_path_validator.return_value = filepath
        result = update_db(filepath, "DB11LITEBIN", VALID_TOKEN, False)
        self.assertIsNone(result, msg="update_db() should return None if the path is not a valid file or is not a binary file")

    @patch('ip2location_toolkit.downloader.update.path_validator')
    def test_filepath_not_file(self, mock_path_validator):
        filepath = "test/path/"
        mock_path_validator.return_value = filepath
        result = update_db(filepath, "DB11LITEBIN", VALID_TOKEN, False)
        self.assertIsNone(result, msg="update_db() should return None if the path is not a valid file or is not a binary file")

    @patch('ip2location_toolkit.downloader.update.path_validator', side_effect=ValueError)
    def test_invalid_path(self, mock_path_validator):
        filepath = "test/path/db.bin"
        result = update_db(filepath, "DB11LITEBIN", VALID_TOKEN, False)
        self.assertIsNone(result, msg="update_db() should return None if the path is invalid (Path Validator raises ValueError)")

    @patch('ip2location_toolkit.downloader.update.new_version_available', return_value=False)
    @patch('ip2location_toolkit.downloader.update.path_validator')
    @patch('ip2location_toolkit.downloader.update.os', wraps=os)
    def test_upto_date_force_false(self, mock_os, mock_path_validator, mock_new_version_available):
        filepath = "test/path/db.bin"
        mock_path_validator.return_value = filepath
        mock_os.path.isfile.return_value = True
        result = update_db(filepath, "DB11LITEBIN", VALID_TOKEN, False)
        self.assertIsNone(result, msg="update_db() should return None if the database is up to date and force is False")

    @patch('ip2location_toolkit.downloader.update.download_extract_db')
    @patch('ip2location_toolkit.downloader.update.new_version_available', return_value=True)
    @patch('ip2location_toolkit.downloader.update.path_validator')
    @patch('ip2location_toolkit.downloader.update.os', wraps=os)
    def test_upto_date_force_true(self, mock_os, mock_path_validator, mock_new_version_available, mock_download_extract_db):
        filepath = "test/path/db.bin"
        mock_path_validator.return_value = filepath
        mock_os.path.isfile.return_value = True
        mock_download_extract_db.return_value = filepath
        result = update_db(filepath, "DB11LITEBIN", VALID_TOKEN, False)
        self.assertEqual(result, filepath, msg="update_db() should return None if the database is up to date and force is False")

    @patch('ip2location_toolkit.downloader.update.download_extract_db', return_value=None)
    @patch('ip2location_toolkit.downloader.update.new_version_available', return_value=True)
    @patch('ip2location_toolkit.downloader.update.path_validator')
    @patch('ip2location_toolkit.downloader.update.os', wraps=os)
    def test_failed_download_extract_db(self,  mock_os, mock_path_validator, mock_new_version_available, mock_download_extract_db):
        filepath = "test/path/db.bin"
        mock_path_validator.return_value = filepath
        mock_os.path.isfile.return_value = True
        result = update_db(filepath, "DB11LITEBIN", VALID_TOKEN, False)
        self.assertIsNone(result, msg="update_db() should return None if the download failed")


    @patch('ip2location_toolkit.downloader.update.download_extract_db')
    @patch('ip2location_toolkit.downloader.update.new_version_available', return_value=True)
    @patch('ip2location_toolkit.downloader.update.path_validator')
    @patch('ip2location_toolkit.downloader.update.os', wraps=os)
    def test_successful_download(self,  mock_os, mock_path_validator, mock_new_version_available, mock_download_extract_db):
        filepath = "test/path/db.bin"
        mock_path_validator.return_value = filepath
        mock_os.path.isfile.return_value = True
        mock_download_extract_db.return_value = 'test/path/new_db.bin'
        result = update_db(filepath, "DB11LITEBIN", VALID_TOKEN, False)
        self.assertEqual(result, 'test/path/new_db.bin', msg="update_db() should return the filepath if the download is successful")
