import os, sys, requests
from pathlib import Path
from tqdm import tqdm
from colorama import Fore
from zipfile import ZipFile



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
    full_path = os.path.join(os.path.dirname(__file__), 'tmp')
    return get_dir_or_create(full_path)


def download_file(url, path):
    chunk_size = 8192
    with requests.get(url, stream=True) as r:
        tqdm_bar = tqdm(unit='B', unit_scale=True, desc="   " + path.split('/')[-1], total=int(r.headers.get('content-length', 0)))
        r.raise_for_status()
        if r.status_code == 404:
            print('   Error downloading {}: Database Not Found.'.format(Fore.RED + path.split('/')[-1] + Fore.RESET))
            return False
        if r.text.startswith('THIS FILE CAN ONLY BE DOWNLOADED'):
            print('   Error downloading {}: Download Limit Exceeded.\n Please try again later.'.format(Fore.RED + path.split('/')[-1] + Fore.RESET))
            return False
        if r.text == 'NO PERMISSION':
            print('   Error downloading {}: Permission Denied.\n Make sure the TOKEN is correct and you have permission to download this database.'.format(Fore.RED + path.split('/')[-1] + Fore.RESET))
            return False
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                tqdm_bar.update(chunk_size)
                f.write(chunk)
    return path

def get_zip_path(file_code):
    tmp_path = get_tmp_dir()
    file_path  = '/'.join([tmp_path, "{filename}.zip".format(filename=file_code)])
    return file_path

def download_zip_db(file_code, token=None):
    if not token:
        raise ValueError('TOKEN is required.')
    url = "https://www.ip2location.com/download?token={}&file={}".format(token, file_code)
    file_path = get_zip_path(file_code)
    print('Downloading {}...'.format(Fore.BLUE + file_code + Fore.RESET))
    try:
        file = download_file(url, file_path)
    except Exception as e:
        print('   Error downloading {}.'.format(Fore.RED + file_code + Fore.RESET))
        raise e
    print('   Downloaded {}.'.format( Fore.GREEN + file_code + Fore.RESET))
    return file

def unzip_db(file_path, output_path=None):
    try:
        with ZipFile(file_path, 'r') as zip_ref:
            to_extract = [f for f in zip_ref.namelist() if f.endswith('.BIN') or f.endswith('.CSV')]
            for f in to_extract:
                print('   Extracting {}...'.format(Fore.BLUE + f + Fore.RESET))
                zip_ref.extract(f, output_path)
    except Exception as e:
        print('   Error unzipping {}.'.format(Fore.RED + file_path.split('/')[-1] + Fore.RESET))
        raise e
    print('   Unzipped {}.'.format(Fore.GREEN + file_path.split('/')[-1] + Fore.RESET))
    return output_path + '/' + to_extract[0]

def download_db(db_code, token=None, output_path=None):
    if not token:
        raise ValueError('TOKEN is required.')
    """
    This function downloads and extract the database with the given code.
    @param db_code The database code.
    """
    file_path = download_zip_db(db_code, token)
    if not file_path:
        print('Failed to download {}.'.format(Fore.RED + db_code + Fore.RESET))
        return
    output_file_path = unzip_db(file_path, output_path)
    return output_file_path