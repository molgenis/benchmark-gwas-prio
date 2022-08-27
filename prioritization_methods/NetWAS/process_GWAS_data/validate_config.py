"""
This module is designed to validate the contents of the configuration file associated
with the script processing the GWAS summstats files for VEGAS.
"""

import linecache
from pathlib import Path
import yaml


class ConfigValidator:
    """
    Class to validate the contents of a configuration file.
    """

    def __init__(self, config) -> None:
        self.config = self.get_config(Path(config))

    @staticmethod
    def get_config(file) -> dict:
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

    def validate_config_file(self) -> None:
        """
        Validate the content of the configuration file.
        """
        self.validate_input_exists()
        self.validate_output_exists()
        self.validate_column_names()

    def validate_input_exists(self) -> None:
        """
        Check if a file exists.
        """
        for info in self.config["traits"].values():
            if not Path(info["file"]).is_file():
                raise FileNotFoundError(f'Input file does not exist:\n{info["file"]}')

    def validate_output_exists(self) -> None:
        """
        Check if the output location exists.
        """
        file = Path(self.config["output"])
        if not file.exists():
            file.mkdir(parents=True)

    def validate_column_names(self) -> None:
        """
        Validate that the given names for the SNP and pvalue columns
        are actually inside of the corresponding file.
        """
        for info in self.config["traits"].values():
            snp = info["columns"]["snp"]
            pval = info["columns"]["pval"]

            if snp == "None" or pval == "None":
                continue

            columns = linecache.getline(info["file"], 1).rstrip().split("\t")

            if not set([snp, pval]).issubset(columns):
                print(f"WARNING! The set value for the SNP and/or p value ({snp}, {pval})"\
                    "column are not found amongst the column names of the corresponding file." \
                    " The program will try to automatically detect the correct column.")


def main():
    """
    Run the main program
    """
    validator = ConfigValidator("config.yaml")
    validator.validate_config_file()


if __name__ == "__main__":
    main()
