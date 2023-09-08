import os
from ..db_codes import CODES

def clear_output():
    try :
        os.system('cls')
    except:
        os.system('clear')

def map_input_to_options(options: list):
    selections = []
    for index, option in enumerate(options):
        selections.append({
            'input': index+1,
            'value': option,
            'prompt': f'{index+1}. {option}'
        })
    return selections

def process_selection_input(selections: list, selection_title: str):
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
    print(f'SELECT {selection_title}:')
    for selection in selections:
        print("   " + selection['prompt'].upper())
    return process_selection_input(selections, selection_title)

def selection_input(title: str, options: list):
    selections = map_input_to_options(options)
    return prompt_selection(selections, title)

def get_code(db_type: str, db_content: str, ip_type: str, db_format: str):
    db_content_index = [idx for idx, db in enumerate(CODES[db_type]) if db['title'] == db_content][0]
    return CODES[db_type][db_content_index][ip_type][db_format]