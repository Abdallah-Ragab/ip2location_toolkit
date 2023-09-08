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
print (get_all_db_codes())


def path_validator(path):
    if not path:
        raise ValueError('Output path is required.')
    if not os.path.exists(path):
        raise ValueError('Output path does not exist.')
    return path

def token_validator(token):
    if not token:
        raise ValueError('The IP2LOCATION token is required. please sign up at https://www.ip2location.com/register to obtain your token.')
    if len(token) != 64:
        raise ValueError('The IP2LOCATION token is invalid. please sign up at https://www.ip2location.com/register to obtain your token.')
    return token

def db_code_validator(db_code):
    if not db_code:
        raise ValueError('The IP2LOCATION database code is required.')
    if db_code not in get_all_db_codes():
        raise ValueError('The IP2LOCATION database code is invalid. Please make sure you have the correct database code.')
    return db_code