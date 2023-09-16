import struct
import datetime


import struct



def version_to_date(version):
    """
    Converts the version number to a date object.

    :param version: The version number in the format "year.month.day".
    :type version: str
    :return: The date object.
    :rtype: datetime.date
    """
    version_set = version.split('.')
    return datetime.date(int(version_set[0])+2000, int(version_set[1]), int(version_set[2]))

def get_db_version(filepath):
    """
    Returns the version of the IP2Location database file.

    :param filepath: The path to the IP2Location database file.
    :type filepath: str
    :return: The version of the IP2Location database file in the format "year.month.day".
    :rtype: str
    """
    file = open(filepath, 'rb')
    file.seek(0)
    header_row = file.read(32)
    year = struct.unpack('B', header_row[2:3])[0]
    month = struct.unpack('B', header_row[3:4])[0]
    day = struct.unpack('B', header_row[4:5])[0]
    return "{}.{}.{}".format(year, month, day)

def new_version_available(filepath):
    current_version = get_db_version(filepath)
    current_version_date = version_to_date(current_version)
    current_date = datetime.date.today()
    month_over = (current_date.year - current_version_date.year) * 12 + current_date.month - current_version_date.month
    if month_over >= 1:
        return True
    return False