import os
from .db_codes import CODES
from ..db_downloader import cli_download_db

def clear_output():
    try :
        os.system('cls')
    except:
        os.system('clear')

def cli_select_db(enable_download = True):

    db_type_options = CODES.keys()
    db_type = selection_input('Database Type', db_type_options)

    db_content_options = [db['title'] for db in CODES[db_type['value']]]
    db_content = selection_input('Database Content', db_content_options)

    ip_type_options = CODES[db_type['value']][0].keys() - ['title']
    ip_type = selection_input('IP Type', ip_type_options)

    db_format_options = CODES[db_type['value']][0][ip_type['value']].keys()
    db_format = selection_input('Database Format', db_format_options)


    db_code = get_code(db_type['value'], db_content['value'], ip_type['value'], db_format['value'])
    if enable_download:
        download_input = input(f'Your Database Code is: {db_code}\nDo you want to download it? (Y/N) ')
        if download_input.lower() == 'y':
            cli_download_db(db_code)
    return db_code

def map_input_to_options(options: list):
    selections = []
    for index, option in enumerate(options):
        selections.append({
            'input': index+1,
            'value': option,
            'prompt': f'{index+1}. {option}'
        })
    return selections

def process_input(selections: list, selection_title: str):
    _input = input('Please select a {title}: '.format(title=selection_title))
    try:
        _input = int(_input)
        selection = list(filter(lambda selection: selection['input'] == _input, selections))[0]
        if not selection:
            raise ValueError
    except (ValueError, IndexError):
        print('Please enter a valid number from the list. \n')
        return process_input(selections, selection_title)
    return selection

def run_selection(selections: list, selection_title: str):
    print(f'SELECT {selection_title}:')
    for selection in selections:
        print("   " + selection['prompt'].upper())
    return process_input(selections, selection_title)

def selection_input(title: str, options: list):
    selections = map_input_to_options(options)
    return run_selection(selections, title)

def get_code(db_type: str, db_content: str, ip_type: str, db_format: str):
    db_content_index = [idx for idx, db in enumerate(CODES[db_type]) if db['title'] == db_content][0]
    return CODES[db_type][db_content_index][ip_type][db_format]