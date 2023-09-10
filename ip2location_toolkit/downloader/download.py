import os, requests
from pathlib import Path
from tqdm import tqdm
from colorama import Fore
from zipfile import ZipFile
from ..exceptions import DataBaseNotFound, DownloadLimitExceeded, DownloadPermissionDenied
from ..validators import token_validator, db_code_validator, path_validator


def get_dir_or_create(path):
    """
    This function checks if the given path exists and if it does not, it creates it.
    @param path The path to check.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_tmp_dir():
    """
    This function returns the path to the temporary directory.
    @return The path to the temporary directory.
    """
    full_path = os.path.join(os.getcwd(), 'tmp')
    return get_dir_or_create(full_path)

def get_downloaded_zip_path(file_code):
    tmp_path = get_tmp_dir()
    file_path  = os.path.join(tmp_path, "{filename}.zip".format(filename=file_code))
    return file_path

def download_file(url, path):
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

def download_database(file_code, token=None):
    try:
        token_validator(token)
    except Exception as e:
        print('Failed to download database. {}'.format(getattr(e, 'message', e)))
        return

    url = "https://www.ip2location.com/download?token={}&file={}".format(token, file_code)
    file_path = get_downloaded_zip_path(file_code)
    print('Downloading {}...'.format(Fore.BLUE + file_code + Fore.RESET))

    try:
        file = download_file(url, file_path)
    except Exception as e:
        print('   Error downloading {}. \n   {}'.format(Fore.RED + file_code + Fore.RESET, getattr(e, 'message', e)))
        return

    print('   Downloaded {}.'.format( Fore.GREEN + file_code + Fore.RESET))
    return file

def unzip_db(file_path, output_path=None):
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
    print('   Extracted {} into {}'.format(Fore.GREEN + extracted_file_path + Fore.RESET, Fore.GREEN + output_path + Fore.RESET))
    return extracted_file_path

def download_extract_db(db_code, token=None, output_path=None):
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
    print(output_file_path)
    return output_file_path