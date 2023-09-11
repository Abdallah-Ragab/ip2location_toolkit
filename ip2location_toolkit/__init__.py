from .cli import run
"""
The IP2Location Toolkit CLI tool is a command-line interface tool that allows users to download IP2Location databases. This module contains the main function that parses command line arguments using the argparse module and then calls the download function with the provided arguments.

Usage:
    python -m ip2location_toolkit --help
    python -m ip2location_toolkit --token <API_TOKEN> --code <DB_CODE> --output <OUTPUT_PATH>

Example:
    python -m ip2location_toolkit --token "YOUR_API_TOKEN" --code "DB1LITEBIN" --output "C:/Users/Downloads"

"""
