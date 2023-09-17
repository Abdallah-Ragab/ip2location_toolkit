from __future__ import annotations
import os, requests
from pathlib import Path
from tqdm import tqdm
from colorama import Fore
from zipfile import ZipFile
from ..exceptions import DataBaseNotFound, DownloadLimitExceeded, DownloadPermissionDenied
from ..validators import token_validator, db_code_validator, path_validator


def get_dir_or_create(path):
    """
    Check if the given path exists. If it does not exist, create it.

    :param path: The path to check and create if necessary.
    :type path: str
    :return: The path that was checked or created.
    :rtype: str
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_tmp_dir():
    """
    This function returns the path to the temporary directory.

    :return: The path to the temporary directory.
    :rtype: str
    """
    full_path = os.path.join(os.getcwd(), '__tmp__')
    return get_dir_or_create(full_path)

def get_downloaded_zip_path(db_code):
    """
    Given a database code, generate the path where the downloaded zip file should be saved.

    :param db_code: The code of the file
    :type db_code: str
    :return: The path where the downloaded zip file should be saved
    :rtype: str
    """
    tmp_path = get_tmp_dir()
    file_path  = os.path.join(tmp_path, "{filename}.zip".format(filename=db_code))
    return file_path

def download_file(url, path):
    """
    Download a file from a given URL and save it to a specified path.

    :param url: the URL of the file to download
    :type url: str
    :param path: the path where the file will be saved
    :type path: str
    :raises DataBaseNotFound: if the file is not found
    :raises DownloadPermissionDenied: if permission to download the file is denied
    :return: the path where the file was saved
    :rtype: str
    """
    request = requests.get(url, stream=True)
    file_length = int(request.headers.get('content-length', 0))
    chunk_size = min(int(file_length / 100), 500000)
    print('   File size: {} MB'.format(format(file_length / 1000000, '.2f')))

    if file_length < 100000:
        if request.status_code == 404:
            raise DataBaseNotFound
        if request.text.startswith('THIS FILE CAN ONLY BE DOWNLOADED'):
            raise DownloadLimitExceeded
        if request.text == 'NO PERMISSION':
            raise DownloadPermissionDenied

    tqdm_bar = tqdm(unit='B', unit_scale=True, desc="   " + path.split('/')[-1], total=file_length)

    with open(path, 'wb') as file:
        for chunk in request.iter_content(chunk_size=chunk_size):
            tqdm_bar.update(len(chunk))
            file.write(chunk)

    return path

def download_database(db_code, token):
    """
    Download a database file from the IP2Location website using a provided database code and a token for authentication.

    :param db_code: The code of the database to download.
    :type db_code: str
    :param token: Token for authentication.
    :type token: str
    :return: The downloaded file.
    :rtype: file
    :raises Exception: If the token is invalid or if there is an error downloading the file.
    """
    try:
        token_validator(token)
    except Exception as e:
        print('Failed to download database. {}'.format(getattr(e, 'message', e)))
        return

    url = "https://www.ip2location.com/download?token={}&file={}".format(token, db_code)
    file_path = get_downloaded_zip_path(db_code)
    print('Downloading {}...'.format(Fore.BLUE + db_code + Fore.RESET))

    try:
        file = download_file(url, file_path)
    except Exception as e:
        print('   Error downloading {}. \n   {}'.format(Fore.RED + db_code + Fore.RESET, getattr(e, 'message', e)))
        return

    print('   Downloaded {}.'.format( Fore.GREEN + db_code + Fore.RESET))
    return file

def rename_file(file_path: str | Path, new_file_name: str) -> Path:
    """
    Rename a file at the given file path to the new file name.

    :param file_path: The path to the file to be renamed.
    :type file_path: str or Path
    :param new_file_name: The new name for the file.
    :type new_file_name: str
    :return: The new file path.
    :rtype: Path
    :raises ValueError: If the file does not exist or the path is not a file.
    :raises Exception: If an error occurs while renaming the file or the file was not renamed.
    """
    old_file_name = Path(file_path).name
    if old_file_name == new_file_name:
        return Path(file_path)

    file_exists = Path(file_path).exists()
    if not file_exists:
        raise ValueError('The file does not exist.')
    is_file = Path(file_path).is_file()
    if not is_file:
        raise ValueError('The path is not a file.')

    file_dir = Path(file_path).parent
    try:
        Path(file_path).rename(Path(file_dir) / new_file_name)
    except Exception as e:
        raise Exception(f'An error occurred while renaming the file: {str(e)}')
    new_file_path = Path(file_dir) / new_file_name
    new_file_exists = new_file_path.exists()
    if not new_file_exists:
        raise Exception('The file was not renamed.')
    return new_file_path

def unzip_db(file_path: str, output_path: str = None) -> str:
    """
    Unzip a database file and extract specific files with extensions `.BIN` or `.CSV` to a specified output path.

    :param file_path: The path to the database file.
    :type file_path: str

    :param output_path: The path to extract the files to (optional). If not specified, the current directory will be used.
    :type output_path: str

    :return: The path to the extracted file.
    :rtype: str
    """
    try:
        with ZipFile(file_path, 'r') as zip_ref:
            extract_list = [f for f in zip_ref.namelist() if f.upper().endswith('.BIN') or f.upper().endswith('.CSV')]
            for f in extract_list:
                print('   Extracting {}...'.format(Fore.BLUE + f + Fore.RESET))
                zip_ref.extract(f, output_path)
    except Exception as e:
        print('   Error unzipping {}.'.format(Fore.RED + file_path.split('/')[-1] + Fore.RESET))
        raise e

    if not output_path:
        output_path = os.path.abspath(Path.cwd())

    extracted_file_path = os.path.join(output_path, extract_list[0])
    print('   Extracted {} into {}'.format(Fore.GREEN + str(extracted_file_path) + Fore.RESET, Fore.GREEN + str(output_path) + Fore.RESET))
    return str(extracted_file_path)

def download_extract_db(db_code, token, output_path=None):
    """
    Download and extract a database given a database code, a token, and an optional output path.

    :param db_code: The code of the database to download.
    :type db_code: str
    :param token: Token for authentication.
    :type token: str
    :param output_path: An optional path to save the downloaded and extracted database.
    :type output_path: str
    :return: The path to the downloaded and extracted database.
    :rtype: str
    :raises: Exception: If the token or database code is invalid, or if there is an error downloading or extracting the database.
    """
    try :
        token_validator(token)
        db_code_validator(db_code)
        path_validator(output_path, required=False)
    except Exception as e:
        print('Failed to download database. {}'.format(getattr(e, 'message', e)))
        return

    file_path = download_database(db_code, token)
    if not file_path:
        return
    output_file_path = unzip_db(file_path, output_path)
    if output_file_path:
        output_file_path = rename_file(output_file_path, db_code + '.BIN')
    return output_file_path