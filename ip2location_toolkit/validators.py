import os
from .db_codes import CODES

def get_all_db_codes():
    all_dbs = CODES['ip2location'] + CODES['ip2proxy']
    all_db_codes = []
    for db in all_dbs:
        for ip_type in ['ipv4', 'ipv6']:
            for db_type in ['cvs', 'bin']:
                all_db_codes.append(db[ip_type][db_type])
    return all_db_codes

def path_validator(path, required=True):
    if not str(path).strip() and required:
        raise ValueError('Output path is required.')
    if not os.path.exists(path) and str(path).strip():
        raise ValueError('Output path does not exist.')
    return path

def token_validator(token, required=True):
    if not token and required:
        raise ValueError('The IP2LOCATION token is required. please sign up at https://www.ip2location.com/register to obtain your token.')
    if len(token) != 64:
        raise ValueError('The IP2LOCATION token is invalid. please sign up at https://www.ip2location.com/register to obtain your token.')
    return token

def db_code_validator(db_code, required=True):
    if not db_code and required:
        raise ValueError('The IP2LOCATION database code is required.')
    if db_code not in get_all_db_codes():
        raise ValueError('The IP2LOCATION database code is invalid. Please make sure you have the correct database code.')
    return db_code