import os
from itertools import chain
from .download import download_extract_db
from ..validators import db_code_validator, token_validator, path_validator


def db_code_prompt(enable_select):
    if enable_select:
        db_code = input("Please Enter The Database code: (Leave blank to select the database from a list) ")
    else:
        db_code = input("Please Enter The Database code: ")

    if enable_select and db_code.strip() == '':
        from .. import cli_select_db
        db_code = cli_select_db(enable_download=False)

    try:
        db_code_validator(db_code)
    except Exception as e:
        print('Error: {}'.format(e.message))
        return db_code_prompt(enable_select)
    return db_code

def token_prompt():
    token = input("Please Enter Your Token: ")
    try:
        token_validator(token)
    except Exception as e:
        print('Error: {}'.format(e.message))
        return token_prompt()
    return token

def output_prompt():
    output = input("Please Enter The Output Path: (Leave blank for current directory)")
    try:
        path_validator(output, required=False)
    except Exception as e:
        print('Error: {}'.format(e.message))
        return output_prompt()
    return output

def cli_download_db(db_code = None, token = None, output = None, enable_select = True):
    if not db_code:
        db_code = db_code_prompt(enable_select)
    if not token:
        token = token_prompt()
    if not output:
        output = output_prompt()
    download_extract_db(db_code, token, output)
