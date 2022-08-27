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
__data__ = "9-8-2022"


class ArgumentParser:
    """
    Class to parse the input arguments.
    """

    def __init__(self):
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
        parser = argparse.ArgumentParser(prog="fisher_exact_test_prio_methods.py",
            description="Python module for performing fisher exact"\
                "tests for gene prioritization methods",
            epilog="Contact: stijnarend@live.nl")

        parser.version = __version__

        parser.add_argument("-c", "--config", action="store",
                           dest="c", required=False, default="config.yaml",
                           help="Location of the configuration file.")

        parser.add_argument("-m", "--method", action="store",
                           dest="m", required=True, choices=["NetWAS", "PoPs", "DEPICT",
                           "MAGMA", "Downstreamer"],
                           help="Name of the prioritization method")

        parser.add_argument("-o", '--output', dest='o',
                        help="Location where the output files need to be stored.",
                        required=True)

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
            Name of command line argument.

        :returns
        --------
        value - Any
            Value of a command line argument
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
        Validate the input files by checking if they actually exists.

        :parameters
        -----------
        input_path - str
            Path to a file
        """
        input_path = Path(input_path)
        self._validate_input_exists(input_path)

    @staticmethod
    def _validate_input_exists(input_path: Path) -> None:
        """
        Check if a file exists.

        :parameters
        -----------
        input_path - Path
            Path to a file
        """
        if not input_path.is_file():
            raise FileNotFoundError(f'Input file does not exist!: {input_path}')
