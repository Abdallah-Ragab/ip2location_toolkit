"""
This module contains functions for validating inputs used in the IP2Location toolkit.

Functions:
    - get_all_db_codes(): Get all the database codes for IP2Location and IP2Proxy databases.
    - path_validator(path, required=True): Validate the given path.
    - token_validator(token): Validate the IP2LOCATION token provided.
    - db_code_validator(db_code): Validate the IP2LOCATION database code provided.
"""
import os
from pathlib import WindowsPath
from .db_codes import CODES



def get_all_db_codes():
    """
    Get all the database codes for IP2Location and IP2Proxy databases.

    :return: A list of all the database codes.
    :rtype: list
    """
    all_dbs = CODES['ip2location'] + CODES['ip2proxy']
    all_db_codes = []
    for db in all_dbs:
        for ip_type in ['ipv4', 'ipv6']:
            for db_type in ['cvs', 'bin']:
                all_db_codes.append(db[ip_type][db_type])
    return all_db_codes

def path_validator(path, required=True):
    """
    Validate the given path.

    :param path: The path to be validated.
    :type path: str or None
    :param required: Whether the path is required or not (default is True).
    :type required: bool
    :raises ValueError: If the path is None and required is True, or if the path is not a string, or if the path is empty and required is True, or if the path does not exist.
    :return: The original path.
    :rtype: str or None
    """
    original_path = path

    if path is None:
        if required:
            raise ValueError('path is required.')
        return None

    try:
        path = str(path)
    except Exception as e:
        raise ValueError('path must be a string. you provided {}'.format(type(path)))

    if not bool(str(path).strip()):
        if required:
            raise ValueError('path is required.')
    else:
        if not os.path.exists(path):
            raise ValueError('path does not exist.')
    return original_path

def token_validator(token):
    """
    Validate the IP2LOCATION token provided.

    :param token: the IP2LOCATION token to validate
    :type token: str
    :raises ValueError: if the token is empty or not 64 characters long
    :return: the validated token
    :rtype: str
    :raises ValueError: if the token is empty or not 64 characters long
    """
    if not bool(str(token).strip()):
        raise ValueError('The IP2LOCATION token is required. please sign up at https://www.ip2location.com/register to obtain your token.')
    if len(token) != 64:
        raise ValueError('The IP2LOCATION token is invalid. please sign up at https://www.ip2location.com/register to obtain your token.')
    return token

def db_code_validator(db_code):
    """
    Validate the IP2LOCATION database code provided.

    :param db_code: the IP2LOCATION database code
    :type db_code: str
    :raises ValueError: if the database code is empty or invalid
    :return: the validated database code
    :rtype: str
    """
    if not bool(str(db_code).strip()):
        raise ValueError('The IP2LOCATION database code is required.')
    if db_code not in get_all_db_codes():
        raise ValueError('The IP2LOCATION database code is invalid. Please make sure you have the correct database code.')
    return db_code