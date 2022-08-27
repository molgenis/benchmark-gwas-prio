"""
Module for parsing arguments.
"""

import sys
import argparse
import os
from pathlib import Path
from typing import Any

__author__ = "Stijn Arends"
__version__ = "v0.1"
__data__ = "21-8-2022"

class ArgumentParser:
    """
    Class to parse the input arguments.
    """

    def __init__(self) -> None:
        self.parser = self._create_argument_parser()
        # Print help if no arguments are supplied and stop the program
        if len(sys.argv) == 1:
            self.parser.print_help(sys.stderr)
            sys.exit(1)
        self.arguments = self.parser.parse_args()

    @staticmethod
    def _create_argument_parser():
        """
        Create an argument parser.

        :returns
        --------
        parser - ArgumentParser
        """
        parser = argparse.ArgumentParser(prog=f"python {os.path.basename(__file__)}",
            description="Python script to parse NetWas results.",
            epilog="Contact: stijnarend@live.nl")

        # Set version
        parser.version = __version__

        parser.add_argument('-f',
            '--file', dest="file",
            help='Input NetWas file - tab seperated txt or csv file',
            required=True)

        parser.add_argument('-t',
            '--threshold', dest="threshold",
            help='NetWas score threshold to select \'good\' reprioritized genes., default = None',
            default=None, type=float)

        parser.add_argument('-o',
            '--output', dest="output",
            help='Location and name of the ouput file.',
            required=True)

        parser.add_argument('--gene_list', dest="gene_list",
            help='Specify if only gene symbols are written out."\
                "Default is NetWas file with filtered genes',
            action="store_true")

        parser.add_argument('-v',
            '--version',
            help='Displays the version number of the script and exitst',
            action='version')

        return parser

    def get_argument(self, argument_key: str) -> Any:
        """
        Method to get an input argument.
        :parameters
        -----------
        argument_key - str
            Full command line argument (so --config for the configuration file argument).

        :returns
        --------
        value - List or boolean
        """
        if self.arguments is not None and argument_key in self.arguments:
            value = getattr(self.arguments, argument_key)
        else:
            value = None
        return value

    def get_parser(self) -> argparse.ArgumentParser:
        """
        Get the argument parser

        :returns
        --------
        parser - argparse.ArgumentParser
            Argument parser
        """
        return self.parser

class CLIArgValidator:
    """
    Class to check if arguments are valid.
    """

    def validate_input_file(self, input_path: str) -> None:
        """
        Validate the input files by checking if they actually exists
        and the which extention they have.

        :parameters
        -----------
        input_path - str
            Path to a file
        """
        input_path = Path(input_path)
        self._validate_input_exists(input_path)
        self._validate_input_extension(input_path)

    @staticmethod
    def _validate_input_exists(input_path: Path) -> None:
        """
        Check if a file exists.

        :parameters
        -----------
        input_path - str
            Path to a file
        """
        if not input_path.is_file():
            raise FileNotFoundError('Input file does not exist!')

    @staticmethod
    def _validate_input_extension(input_path: Path) -> None:
        """
        Check if a file has the right extension.

        :parameters
        -----------
        input_path - str
            Path to a file
        """
        if not input_path.suffix in [".txt", ".csv"]:
            raise FileNotFoundError('Input file should be either a .txt or .csv')
