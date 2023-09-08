class DataBaseNotFound(Exception):
    message = 'The database you are trying to download does not exist on IP2LOCATION.'

class DownloadLimitExceeded(Exception):
    message = 'You have exceeded the download limit set by IP2LOCATION for this database. Please try again later.'

class DownloadPermissionDenied(Exception):
    message = 'You do not have permission to download this database. Please make sure you have the correct TOKEN and you have permission to download this database.'
