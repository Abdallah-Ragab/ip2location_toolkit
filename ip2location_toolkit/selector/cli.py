import os
from ..db_codes import CODES

def clear_output():
    """
    Clear the output in the console by executing the appropriate command based on the operating system.
    @return None
    """
    try :
        os.system('cls')
    except:
        os.system('clear')

def map_input_to_options(options: list):
    """
    Given a list of options, map each option to a dictionary with the following keys:
    - 'input': the index of the option plus 1
    - 'value': the option itself
    - 'prompt': a string that combines the index plus 1, a period, and the option
    @param options - a list of options
    @return a list of dictionaries, each representing an option with the keys 'input', 'value', and 'prompt'
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
    @param selections - a list of selections to choose from
    @param selection_title - the title of the selection
    @return The selected item from the list
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
    @param selections - a list of selections, each containing a prompt
    @param selection_title - the title of the selection
    @return the selected option
    """
    print(f'SELECT {selection_title}:')
    for selection in selections:
        print("   " + selection['prompt'].upper())
    return process_selection_input(selections, selection_title)

def selection_input(title: str, options: list):
    """
    Prompt the user to select an option from a given list of options.
    @param title - the title of the selection prompt
    @param options - a list of options to choose from
    @return the selected option
    """
    selections = map_input_to_options(options)
    return prompt_selection(selections, title)

def get_code(db_type: str, db_content: str, ip_type: str, db_format: str):
    """
    Given the type of database (IP2LOCATION, IP2PROXY), the content of the database, the type of IP (v4, v6), and the format of the database (CSV, BIN), retrieve the corresponding code from the CODES dictionary.
    @param db_type - the type of database
    @param db_content - the content of the database
    @param ip_type - the type of ip (v4, v6)
    @param db_format - the format of the database
    @return The code corresponding to the given parameters
    """
    db_content_index = [idx for idx, db in enumerate(CODES[db_type]) if db['title'] == db_content][0]
    return CODES[db_type][db_content_index][ip_type][db_format]