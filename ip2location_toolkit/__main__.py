"""
The IP2Location Toolkit CLI tool is a command-line interface tool that allows users to download IP2Location databases. This module contains the main function that parses command line arguments using the argparse module and then calls the download function with the provided arguments.

Usage:
    python -m ip2location_toolkit --help
    python -m ip2location_toolkit --token <API_TOKEN> --code <DB_CODE> --output <OUTPUT_PATH>

Example:
    python -m ip2location_toolkit --token "YOUR_API_TOKEN" --code "DB1LITEBIN" --output "C:\Users\Downloads"

"""

import argparse
from pathlib import Path
from .cli import download

def main():
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

if __name__ == '__main__':
    main()