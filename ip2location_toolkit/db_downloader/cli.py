import os
from itertools import chain
from .download import download_db


def db_code_prompt(enable_select):
    from ..db_selector import DB_CODES

    all_db_codes = list(chain.from_iterable(
        (i['ipv4']['cvs'], i['ipv4']['bin'], i['ipv6']['cvs'], i['ipv6']['bin'])
        for i in  list(chain.from_iterable(DB_CODES.values()))
    ))
    if enable_select:
        db_code = input("Please Enter The Database code: (Leave blank to select the database from a list) ")
    else:
        db_code = input("Please Enter The Database code: ")

    if enable_select and db_code.strip() == '':
        from .. import cli_select_db
        db_code = cli_select_db(enable_download=False)

    return validate_db_code(db_code, all_db_codes, enable_select)

def validate_db_code(db_code, all_db_codes, enable_select):
    try:
        if db_code not in all_db_codes:
            raise ValueError
    except ValueError:
        print('Incorrect Database Code. Please enter a valid Database code. \n')
        return db_code_prompt(enable_select)
    return db_code


def token_prompt():
    token = input("Please Enter Your Token: ")
    try:
        if len(token) != 64:
            raise ValueError
    except ValueError:
        print('Incorrect TOKEN. Please enter a valid token. \n')
        return token_prompt()
    return token

def output_prompt():
    output = input("Please Enter The Output Path: (Leave blank for current directory)")
    try:
        if output.strip() and not os.path.exists(output):
            raise ValueError
    except ValueError:
        print('Directory does not exist. Please enter a valid output path. \n')
        return output_prompt()
    return output

def cli_download_db(db_code = None, token = None, output = None, enable_select = True):
    if not db_code:
        db_code = db_code_prompt(enable_select)
    if not token:
        token = token_prompt()
    if not output:
        output = output_prompt()
    download_db(db_code, token, output)
