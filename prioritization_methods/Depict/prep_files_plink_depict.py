"""
This module prepares files for PLINK and DEPICT.
"""

import gzip
from pathlib import Path
import yaml
import pandas as pd


def prep_plink(file) -> None:
    """
    Function to prepare IBD (Inflammatory bowel disease) and PC (Prostate cancer) files
    Only loads in the usefull columns
    renames all columns so Plink will recognize them
    """
    col_list = ["chromosome", "base_pair_location", "variant_id", "beta", "standard_error", "p_value"]
    if file.rsplit(".", 1)[1] == "gz":
        with gzip.open(file, "rb") as f:
            data = pd.read_csv(f, sep="\s+", usecols=col_list)
    else:
        data = pd.read_csv(file, sep="\s+", usecols=col_list)
    
    data = data.rename(columns={"chromosome":"CHR", "base_pair_location":"POS", "variant_id":"SNP", "beta":"BETA", "standard_error":"SE", "p_value":"P"})
    file = file.split(".", 1)[0]
    data.to_csv(file + "_prepped.txt", sep="\t", index=False)


def prep_for_depict(file) -> str:
    """
    Removes all columns except SNP. this is needed for Depict
    run for IBD, PC, and Height file
    """
    data = pd.read_csv(file, sep="\s+")
    data = data["SNP"]
    file = file.split(".", 1)[0]
    new_file = file + "_prepped4depict.txt"
    data.to_csv(new_file, sep="\t", index=False, header=False)
    return new_file


def downsample_file(file) -> None:
    """
    The Height SNP file is too large for Depict.
    Therefor it was found it could not have more than 200 SNP's
    Takes 200 random SNP's from Height file to use in Depict and saves this to Height_200.txt
    """
    data = pd.read_csv(file, sep="\t")
    data = data.sample(n=200, axis=0)
    path = file.rsplit("/", 1)[0]
    if path == file:
        path = ""
    data.to_csv(path + "/Height_200.txt", sep="\t", index=False, header=False)


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

def main():
    config = get_config("config.yaml")
    for _, file in config["plink"]:
        prep_plink(file)

    IBD_prepped = prep_for_depict(config["DEPICT"]["IBD"])
    PrC_prepped = prep_for_depict(config["DEPICT"]["PrC"])
    height_prepped = prep_for_depict(config["DEPICT"]["Height"])

    downsample_file(height_prepped)



if __name__ == "__main__":
    main()