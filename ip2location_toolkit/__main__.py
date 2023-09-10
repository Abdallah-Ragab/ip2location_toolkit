import argparse
from pathlib import Path
from .cli import download

def main():
    """
    The main function of the IP2Location Toolkit CLI tool. It parses command line arguments using the argparse module and then calls the download function with the provided arguments.
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

if __name__ == '__main__':
    main()