"""
Perform multiple fisher exact tests for a number of prioritization methods.
"""

import sys
import os
# from dataclasses import dataclass
from pathlib import Path
# import numpy as np
import pandas as pd
# from scipy import stats
# import scipy.stats as stats
import yaml


root_dir = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir,
                  os.pardir))

sys.path.insert(0, root_dir)

from utils.prioritization_methods import Downstreamer, Magma, Depict, PoPs, NetWAS
from utils.fisher import HPO, FisherTest
from arg_parser import ArgumentParser, CLIArgValidator


__author__ = "Stijn Arends"
__version__ = "v0.1"
__data__ = "9-8-2022"


def get_config(file: Path) -> dict:
    """
    Read in config file and return it as a dictionary.

    :parameter
    ----------
    file - str
        Configuration file in yaml format

    :returns
    --------
    config - dict
        Configuration file in dictionary form.
    """
    if not file.exists():
        raise FileExistsError(f"The file that was supplied does not exists: {file}")

    with open(file, 'r', encoding="utf-8") as stream:
        config = yaml.safe_load(stream)

    return config


def read_hpo_info(hpo_info: pd.DataFrame) -> pd.DataFrame:
    """
    Read in a CSV file containing information about HPO terms
    and related GWAS traits.

    :parameter
    ----------
    hpo_info - str
        CSV containing info about hpo/GWAS traits
    """
    hpo_info_data = pd.read_csv(hpo_info, sep=",")
    return hpo_info_data


def make_out_dir(path: Path) -> None:
    """
    Create a directory (if it does not exsit yet) to store the
    data.

    :parameter
    ----------
    path - Path
        Location of directory

    :Excepts
    --------
    FileExistsError
        The directory already exists
    """
    try:
        path.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print(f"[{make_out_dir.__name__}] {path} already exists.")


def write_out_data(data: pd.DataFrame, file: Path) -> None:
    """
    Write out a pandas data frame to a file.

    :parameters
    -----------
    data - pd.DataFrame
        Data
    file - Path
        Name and location of output file
    """
    data.to_csv(file, sep="\t")


def main():
    """
    Run the program.
    """
    arg_parse = ArgumentParser()

    config_file = arg_parse.get_argument("c")
    method = arg_parse.get_argument("m")
    output_dir = arg_parse.get_argument("o")

    cli_validator = CLIArgValidator()
    cli_validator.validate_input_file(config_file)

    config = get_config(Path(config_file))

    out_dir = Path(output_dir) / method

    make_out_dir(out_dir)

    hpo_data = config["hpo_data"]
    hpo_info_data = read_hpo_info(Path(config["hpo_info"]))

    methods = {"NetWAS": NetWAS, "PoPs": PoPs, "DEPICT": Depict,
                "Downstreamer": Downstreamer, "MAGMA":Magma}

    hpo = HPO(database=hpo_data)
    fisher = FisherTest()

    method_instance = methods[method](hpo=hpo, fisher=fisher)

    for trait, file in config["traits"].items():
        print(f"Processing trait: {trait}")
        file = Path(file)

        method_data, genes = method_instance.read_data(file)

        overlap_hpo, overlap_genes, _ = method_instance.get_overlap(hpo.hpo_data, genes)

        overlap_method = method_instance.get_overlap_genes(method_data, overlap_genes)

        _, sig_genes = method_instance.filter_data(overlap_method)

        fish_results = method_instance.fisher.perform_fisher_exact_tests(overlap_hpo,
                                    sig_genes, hpo_info_data)

        out_file = out_dir / ("fisher_result_" + file.stem + ".csv")

        write_out_data(fish_results, out_file)


if __name__ == "__main__":
    main()
