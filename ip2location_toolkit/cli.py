"""
This module provides a command-line interface for the IP2Location Toolkit.

It includes functions for downloading and selecting IP2Location databases.

Functions:
    download: Downloads the IP2Location database file using the specified database code and token.
    select: Prompts the user to select a database type, content, IP type, and database format.
"""

from .downloader.download import download_extract_db
from .downloader.cli import db_code_prompt, token_prompt, output_prompt
from .selector.cli import selection_input, get_code
from .db_codes import CODES
import argparse
from pathlib import Path


def run():
    """
    The main function of the IP2Location Toolkit CLI tool. It parses command line arguments using the argparse module and then calls the download function with the provided arguments.

    :return: None
    """
    parser = argparse.ArgumentParser(description='IP2Location Toolkit: A CLI tool to download IP2Location databases.')
    parser.add_argument('--token', '-t', help='Your IP2Location API Token')
    parser.add_argument('--code', '-c', help='Database code to download')
    parser.add_argument('--output', '-o', help='Output directory', type=Path)
    args = parser.parse_args()

    if args.code:
        db_code = args.code
    else:
        db_code = None

    if args.output:
        output_path = args.output
    else:
        output_path = None

    if args.token:
        token = args.token
    else:
        token = None

    download(db_code, token, output_path)


def download(db_code=None, token=None, output=None, enable_select=True):
    """
    Downloads the IP2Location database file using the specified database code and token.

    :param db_code: The database code to download. If not provided, the user will be prompted to select a database.
    :type db_code: str
    :param token: The token to use for authentication. If not provided, the user will be prompted to enter a token.
    :type token: str
    :param output: The output file path to save the downloaded database file. If not provided, the user will be prompted to enter a file path.
    :type output: str
    :param enable_select: Whether to enable the database selection prompt. Defaults to True.
    :type enable_select: bool

    :return: None
    :rtype: None
    """
    if not db_code:
        db_code = db_code_prompt(enable_select)
    if not token:
        token = token_prompt()
    if not output:
        output = output_prompt()
    download_extract_db(db_code, token, output)


def select(enable_download=True):
    """
    Prompts the user to select a database type, content, IP type, and database format.
    Retrieves the corresponding code for the selected options and prompts the user to download it.

    :param enable_download: A boolean value indicating whether to prompt the user to download the code or not. Default is True.
    :type enable_download: bool
    :return: The database code for the selected options.
    :rtype: str
    """
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
