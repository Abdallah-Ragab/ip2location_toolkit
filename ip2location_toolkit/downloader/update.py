import struct
import datetime, os, pathlib
from ..validators import path_validator

def get_db_header(filepath):
    """
    Returns the header of the IP2Location database file.

    :param filepath: The path to the IP2Location database file.
    :type filepath: str
    :return: The header of the IP2Location database file.
    :rtype: bytes
    """
    try:
        filepath = path_validator(filepath)
        with open(filepath, 'rb') as file:
            file.seek(0)
            header = file.read(30)
        if len(header) != 30:
            raise ValueError("Invalid database file (less than 30 bytes)")
        return header
    except IOError as e:
        raise ValueError('Failed to obtain Database Header: Error occurred during file operations ({})'.format(str(e)))
    except ValueError as e:
        raise ValueError('Failed to obtain Database Header: Invalid Database Path ({})'.format(str(e)))

def version_to_date(version):
    """
    Converts the version number to a date object.

    :param version: The version number in the format "year.month.day".
    :type version: str
    :return: The date object.
    :rtype: datetime.date
    """
    try:
        version_set = version.split('.')
        if len(version_set) != 3:
            raise ValueError("Invalid version format")
        return datetime.date(int(version_set[0])+2000, int(version_set[1]), int(version_set[2]))
    except (ValueError, IndexError):
        raise ValueError("Invalid version format")

def get_db_version(filepath):
    """
    Returns the version of the IP2Location database file.

    :param filepath: The path to the IP2Location database file.
    :type filepath: str
    :return: The version of the IP2Location database file in the format "year.month.day".
    :rtype: str
    """
    db_header = get_db_header(filepath)
    year, month, day = struct.unpack('BBB', db_header[2:5])
    return f"{year}.{month}.{day}"

def new_version_available(filepath):
    current_version = get_db_version(filepath)
    current_version_date = version_to_date(current_version)
    current_date = datetime.date.today()
    month_over = int((current_date.year - current_version_date.year) * 12 + (current_date.month - current_version_date.month))
    if month_over >= 1:
        return True
    return False
