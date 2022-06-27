#!/usr/bin/env python

"""
Module for parsing the results produced by NetWAS.
"""

# from itertools import tee
import sys
import argparse
from typing import Any
from pathlib import Path
import os
# from xmlrpc.client import Boolean
import pandas as pd


__author__ = "Stijn Arends"
__version__ = "v0.1"
__date__ = "20-5-2022"


class NetWasParser:
    """
    A class to parse the results produced by NetWAS.

    link: https://hb.flatironinstitute.org/netwas
    """

    def __init__(self, file: Path, output_file: Path) -> None:
        self.file = file
        self.output_file = output_file

    def parse_data(self, threshold: float, gene_list: bool) -> None:
        """
        Parse a NetWas file to extract only the nominal positive genes.
        
        :paramters
        ----------
        threshold - float
            Threshold to decide which gene to keep - used on the NetWas score column
        gene_list - Boolean
            Flag specifying wheter or not to write out all the columns or only the gene names - default = False
                True - only gene names
                False - all columns
        """
        df = self.read_netwas_data(self.file)
        filtered_df = self.get_prioritized_genes(df, threshold)
        if gene_list:
            df_genes = pd.DataFrame(filtered_df.Gene)
            self.write_netwas_data(df_genes, self.output_file)
        else:
            self.write_netwas_data(filtered_df, self.output_file)

    @staticmethod
    def read_netwas_data(file: Path) -> pd.DataFrame:
        """
        Read in a NetWas result file 

        :parameters
        -----------
        file - Path
            File containing NetWas results
        """
        df = pd.read_csv(file, sep=None, skiprows=28, names= ["Gene", "label", "score"], engine='python')
        return df

    def get_prioritized_genes(self, df:pd.DataFrame, threshold:float) -> pd.DataFrame:
        """
        Only keep the genes with a NetWas score higher or equal to the threshold

        :parameters
        -----------
        df - pd.DataFrame
            NetWas data inside a pandas data frame - columns: [Genes, label, score]
        threshold - float
            Threshold to filter the data on.

        :returns
        --------
        df - pd.DataFrame
            Filtered NetWas data
        """
        if threshold:
            return df[df.score >= threshold]
        return df

    def write_netwas_data(self, data: pd.DataFrame, output_file: Path) -> None:
        """
        Write NetWas data to an output file.

        :parameters
        -----------
        data - pd.DataFrame
            NetWas data
        output_file - Path
            Name and location of the output file
        """
        self.make_data_dir(output_file)
        data.to_csv(output_file, sep="\t", index=False, header=False)

    def make_data_dir(self, dir: Path) -> None:
        """
        Create a directory (if it does not exisit yet) to store the 
        data.

        :Excepts
        --------
        FileExistsError
            The directory already exists
        """
        try:
            dir.parent.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            pass

    
class ArgumentParser:
    """
    Class to parse the input arguments.
    """

    def __init__(self) -> None:
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
            help='Specify if only gene symbols are written out. Default is NetWas file with filtered genes',
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


class CLIArgValidator:
    """
    Class to check if arguments are valid.
    """

    def validate_input_file(self, input_path: str) -> None:
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


def main():
    arg_parser = ArgumentParser()
    arg_validator = CLIArgValidator()
    file = arg_parser.get_argument('file')
    threshold = arg_parser.get_argument('threshold')

    output_file = Path(arg_parser.get_argument('output'))
    gene_list = arg_parser.get_argument("gene_list")
    arg_validator.validate_input_file(file)

    net_was = NetWasParser(file=file, output_file=output_file)

    net_was.parse_data(threshold=threshold, gene_list=gene_list)


if __name__ == "__main__":
    main()