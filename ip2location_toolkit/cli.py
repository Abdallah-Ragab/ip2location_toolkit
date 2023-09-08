from .downloader.download import download_extract_db
from .downloader.cli import db_code_prompt, token_prompt, output_prompt
from .selector.cli import selection_input, get_code
from .db_codes import CODES


def download(db_code = None, token = None, output = None, enable_select = True):
    if not db_code:
        db_code = db_code_prompt(enable_select)
    if not token:
        token = token_prompt()
    if not output:
        output = output_prompt()
    download_extract_db(db_code, token, output)


def select(enable_download = True):

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
            download(db_code)
    return db_code
