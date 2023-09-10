"""
This module contains functions for processing user input for selecting an item from a list of selections.

Functions:
    clear_output() -> None
    map_input_to_options(options: list) -> list
    process_selection_input(selections: list, selection_title: str) -> dict
    prompt_selection(selections: list, selection_title: str) -> Any
    selection_input(title: str, options: list) -> Any
    get_code(db_type: str, db_content: str, ip_type: str, db_format: str) -> str
"""
import os
from ..db_codes import CODES



def clear_output():
    """
    Clear the output in the console by executing the appropriate command based on the operating system.

    :return: None
    :rtype: None
    """
    try :
        os.system('cls')
    except:
        os.system('clear')

def map_input_to_options(options: list):
    """
    Given a list of options, map each option to a dictionary with the following keys:

    Each dictionary in the returned list has the following keys:
    - 'input': the index of the option plus 1
    - 'value': the option itself
    - 'prompt': a string that combines the index plus 1, a period, and the option

    :param options: a list of options
    :type options: list

    :return: a list of dictionaries, each representing an option with the keys 'input', 'value', and 'prompt'
    :rtype: list

    """
    selections = []
    for index, option in enumerate(options):
        selections.append({
            'input': index+1,
            'value': option,
            'prompt': f'{index+1}. {option}'
        })
    return selections

def process_selection_input(selections: list, selection_title: str):
    """
    Process the user's input for selecting an item from a list of selections.

    :param selections: A list of selections to choose from.
    :type selections: list
    :param selection_title: The title of the selection.
    :type selection_title: str
    :return: The selected item from the list.
    :rtype: dict
    :raises ValueError: If the input is not a valid number from the list.
    :raises IndexError: If the input is not a valid number from the list.
    """
    _input = input('Please select a {title}: '.format(title=selection_title))
    try:
        _input = int(_input)
        selection = list(filter(lambda selection: selection['input'] == _input, selections))[0]
        if not selection:
            raise ValueError
    except (ValueError, IndexError):
        print('Please enter a valid number from the list. \n')
        return process_selection_input(selections, selection_title)
    return selection

def prompt_selection(selections: list, selection_title: str):
    """
    Display a list of selections with a given title and prompt the user to make a selection.

    :param selections: A list of selections, each containing a prompt.
    :type selections: list
    :param selection_title: The title of the selection.
    :type selection_title: str
    :return: The selected option.
    :rtype: Any
    """
    print(f'SELECT {selection_title}:')
    for selection in selections:
        print("   " + selection['prompt'].upper())
    return process_selection_input(selections, selection_title)

def selection_input(title: str, options: list):
    """
    Prompt the user to select an option from a given list of options.

    :param title: The title of the selection prompt.
    :type title: str
    :param options: A list of options to choose from.
    :type options: list
    :return: The selected option.
    :rtype: Any

    """
    selections = map_input_to_options(options)
    return prompt_selection(selections, title)

def get_code(db_type: str, db_content: str, ip_type: str, db_format: str):
    """
    Given the type of database (IP2LOCATION, IP2PROXY), the content of the database, the type of IP (v4, v6), and the format of the database (CSV, BIN), retrieve the corresponding code from the CODES dictionary.

    :param db_type: The type of database
    :type db_type: str
    :param db_content: The content of the database
    :type db_content: str
    :param ip_type: The type of IP (v4, v6)
    :type ip_type: str
    :param db_format: The format of the database
    :type db_format: str
    :return: The code corresponding to the given parameters
    :rtype: str
    """
    db_content_index = [idx for idx, db in enumerate(CODES[db_type]) if db['title'] == db_content][0]
    return CODES[db_type][db_content_index][ip_type][db_format]