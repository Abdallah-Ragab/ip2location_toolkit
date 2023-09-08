from ..validators import db_code_validator, token_validator, path_validator
from colorama import Fore

RED = Fore.RED
BLUE = Fore.BLUE
GREEN = Fore.GREEN
RESET = Fore.RESET


def db_code_prompt(enable_select):
    if enable_select:
        db_code = input("Please Enter The Database code: (Leave blank to select the database from a list) ")
    else:
        db_code = input("Please Enter The Database code: ")

    if enable_select and db_code.strip() == '':
        from ..cli import select
        db_code = select(enable_download=False)

    try:
        db_code_validator(db_code)
    except Exception as e:
        print(RED + 'Error:' + RESET + '{}'.format(getattr(e, 'message', e)))
        return db_code_prompt(enable_select)
    return db_code

def token_prompt():
    token = input("Please Enter Your Token: ")
    try:
        token_validator(token)
    except Exception as e:
        print(RED + 'Error:' + RESET + '{}'.format(getattr(e, 'message', e)))
        return token_prompt()
    return token

def output_prompt():
    output = input("Please Enter The Output Path: (Leave blank for current directory)")
    try:
        path_validator(output, required=False)
    except ValueError as e:
        print(RED + 'Error:' + RESET + '{}'.format(getattr(e, 'message', e)))
        return output_prompt()
    return output
