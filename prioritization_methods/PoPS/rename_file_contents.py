#!/usr/bin/env python3

"""
Edit feature files by adding a prefix to the file and columns names.
This is to make each file unique, which is neccesary to run PoPs.

Author - Stijn Arends
Date - 15-6-2022
"""

import multiprocessing as mp
import pandas as pd
import os
from pathlib import Path
import argparse
import sys

__version__ = "V0.1"

class EditFeatureFiles:

    def __init__(self, folder, prefix):
        self.folder = Path(folder)
        self.prefix = prefix

    def edit_file(self, file:str) -> None:
        """
        Edit a file by adding a prefix to the file name, and 
        column names.

        :parameters
        file - str
            Name of a file
        """
        print(f"Processing: {file}")
        old_file = self.folder / file
        new_name = (self.prefix + file)
        new_file = self.folder / new_name

        self.rename_file(old_file, new_file)

        df = self.read_data(new_file)
        df = self.rename_col_names(df, new_name)

        self.write_data(df, new_file)

    @staticmethod
    def rename_file(old:Path, new:Path) -> None:
        """
        Rename a file.

        :parameters
        -----------
        old - Path
            Old file name
        new - Path
            New file name
        """
        os.rename(old, new)

    def read_data(self, file:Path) -> pd.DataFrame:
        """
        Read in the feature data as either a gz file or normal txt file.

        :parameters
        -----------
        file - Path
            A file
        gz -bool
            If the file is gziped or not

        :returns
        --------
        df - pd.DataFrame
            data in a pandas data frame
        """
        df = pd.read_csv(file, sep="\t", header=0)
        return df

    def rename_col_names(self, df: pd.DataFrame, name:Path) -> pd.DataFrame:
        """
        Rename the columns of the features by adding the file name
        to the front of the columns. 

        :parameters
        -----------
        df - pd.DataFrame
            Data in a data frame
        name - Path
            Name of the file to use as prefix of the columns

        :returns
        --------
        df - pd.DataFrame
            data with renamed columns
        """
        filename = Path(name)
        base, _, _ = filename.name.partition('.')
        base_name = str(filename.with_name(base))

        new_cols = [base_name + "_" + column for column in df.columns[1:].values]
        df.columns.values[1:] = new_cols
        return df

    def write_data(self, df:pd.DataFrame, file_name: Path) -> None:
        """
        Overwrite the old data with the new data.

        :parameters
        -----------
        df - pd.DataFrame
            Data in a data frame
        file_name - Path
            A file
        gz -bool
            If the file is gziped or not
        """
        df.to_csv(file_name, sep="\t", index=False, mode="w+")


class ArgumentParser:
    """
    Class to parse the input arguments.
    """

    def __init__(self):
        parser = self._create_argument_parser()
        # Print help if no arguments are supplied and stop the program
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)
        self.arguments = parser.parse_args()

    @staticmethod
    def _create_argument_parser():
        """
        Create an argument parser.
        
        :returns
        --------
        parser - ArgumentParser
        """
        parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
            description="Edit feature files for PopS by adding a prefix to the file and column names.",
            epilog="Contact: stijnarend@live.nl")

        # Set version
        parser.version = __version__

        parser.add_argument('-d',
            '--directory', dest='directory',
            help='Location of the directory containing the features.')

        parser.add_argument('--prefix', type=str, dest="prefix",
            help='Prefix to use when renaming the files and columns. Default = pops_',
            default="pops_")

        parser.add_argument('-v',
            '--version',
            help='Displays the version number of the script and exitst',
            action='version')

        return parser

    def get_argument(self, argument_key):
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


class CommandLineArgumentsValidator:
    """
    Class to check if arguments are valid.
    """

    def validate_input_path(self, input_path):
        self._validate_input_exists(input_path)

    @staticmethod
    def _validate_input_exists(input_path):
        """
        Check if a file exists. 
        :parameters
        -----------
        input_path - str
            Path to a directory
        """
        if not Path(input_path).is_dir():
            raise FileNotFoundError('Input directory does not exist!')


def main():

    cla_parser = ArgumentParser()
    folder = cla_parser.get_argument('directory')
    prefix = cla_parser.get_argument('prefix')

    # Validate passed arguments
    cla_validator = CommandLineArgumentsValidator()
    cla_validator.validate_input_path(folder)

    edit_files = EditFeatureFiles(folder=folder, prefix=prefix)

    files = os.listdir(folder)
    
    with mp.Pool(mp.cpu_count()) as p:
        p.map(edit_files.edit_file, files)


if __name__ == "__main__":
    main()

