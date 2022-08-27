#!/usr/bin/env python

"""
Module for parsing the results produced by NetWAS.
"""

from pathlib import Path
import pandas as pd
from arg_parser import ArgumentParser, CLIArgValidator


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
            Flag specifying wheter or not to write out all the columns or only the gene names
                - default = False
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
        df = pd.read_csv(file, sep=None, skiprows=28,
                        names= ["Gene", "label", "score"], engine='python')
        return df

    @staticmethod
    def get_prioritized_genes(df:pd.DataFrame, threshold:float) -> pd.DataFrame:
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

    @staticmethod
    def make_data_dir(directory: Path) -> None:
        """
        Create a directory (if it does not exisit yet) to store the
        data.

        :Excepts
        --------
        FileExistsError
            The directory already exists
        """
        try:
            directory.parent.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            pass


def main():
    """
    Run the main program.
    """
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
