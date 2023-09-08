from . import cli_download_db
import argparse
from pathlib import Path

def main():
    """
    The main function of the IP2Location Toolkit. The interface for the cli tool.
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

    cli_download_db(db_code, token, output_path)

if __name__ == '__main__':
    main()