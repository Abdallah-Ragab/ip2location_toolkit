"""
This module contains functions for prompting the user to enter database code, token and output path.
It also validates the user input using the corresponding validators.
"""

from ..validators import db_code_validator, token_validator, path_validator
from colorama import Fore

RED = Fore.RED
BLUE = Fore.BLUE
GREEN = Fore.GREEN
RESET = Fore.RESET


def db_code_prompt(enable_select):
    """
    Prompt the user to enter a database code.

    If `enable_select` is `True`, the user can choose to either enter the code manually or select a database from a list.
    If `enable_select` is `False`, the user must enter the code manually.

    :param enable_select: A boolean value indicating whether to enable the user to select a database from a list.
    :return: The database code entered by the user.
    """
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
    """
    Prompt the user to enter a token and validate it using the `token_validator` function. If the token is invalid, display an error message and prompt the user again. Once a valid token is entered, return it.

    :return: The validated token
    :rtype: str
    """
    token = input("Please Enter Your Token: ")
    try:
        token_validator(token)
    except Exception as e:
        print(RED + 'Error:' + RESET + '{}'.format(getattr(e, 'message', e)))
        return token_prompt()
    return token

def output_prompt():
    """
    Prompt the user to enter the output path. If the user leaves it blank, the current directory will be used as the output path.
    Validate the entered path using the `path_validator` function. If the entered path is not valid, display an error message and prompt the user again.
    Return the validated output path.

    :return: A string representing the validated output path.
    """
    output = input("Please Enter The Output Path: (Leave blank for current directory)")
    try:
        path_validator(output, required=False)
    except ValueError as e:
        print(RED + 'Error:' + RESET + '{}'.format(getattr(e, 'message', e)))
        return output_prompt()
    return output
