

"""
This module defines custom exception classes for handling errors related to IP2Location databases.

The following exception classes are defined:
- DataBaseNotFound: Raised when the database being downloaded does not exist on IP2LOCATION.
- DownloadLimitExceeded: Raised when the download limit set by IP2LOCATION for a database has been exceeded.
- DownloadPermissionDenied: Raised when a user does not have permission to download a database.
"""

class DataBaseNotFound(Exception):
    """
    An exception class to handle the case when the database being downloaded does not exist on IP2LOCATION.
    The exception message is "The database you are trying to download does not exist on IP2LOCATION."
    """
    message = 'The database you are trying to download does not exist on IP2LOCATION.'

class DownloadLimitExceeded(Exception):
    """
    An exception class for handling cases where the download limit set by IP2LOCATION for a database has been exceeded.
    The exception message is set to "You have exceeded the download limit set by IP2LOCATION for this database. Please try again later."
    """
    message = 'You have exceeded the download limit set by IP2LOCATION for this database. Please try again later.'

class DownloadPermissionDenied(Exception):
    """
    An exception class that is raised when a user does not have permission to download a database.
    The exception message is set to "You do not have permission to download this database. Please make sure you have the correct TOKEN and you have permission to download this database."
    """
    message = 'You do not have permission to download this database. Please make sure you have the correct TOKEN and you have permission to download this database.'
