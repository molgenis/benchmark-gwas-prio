"""
Perform fisher's exact tests on the results from a number of prioritization methods.
"""

import sys
import os
from pathlib import Path
from typing import Tuple
import numpy as np
import yaml
from matplotlib_venn import venn2, venn2_circles
import matplotlib.pyplot as plt


root_dir = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir,
                  os.pardir))

sys.path.insert(0, root_dir)

from fisher_tests.single_test.arg_parser import ArgumentParser, CLIArgValidator
from utils.prioritization_methods import Downstreamer, Magma, Depict, PoPs, NetWAS
from utils.fisher import HPO, FisherTest


class VennDiagram:
    """
    Create a venn diagram that can be displayed
    or saved to disc.
    """

    def __init__(self, n_sig_genes, n_hpo_term_genes, overlap_sig_hpo) -> None:
        self.n_sig_genes = n_sig_genes
        self.n_hpo_term_genes= n_hpo_term_genes
        self.overlap_sig_hpo = overlap_sig_hpo

    def __plot_venn_diagram(self) -> None:
        """
        Plot a venn diagram with three circles
        """
        venn2(subsets=(self.n_sig_genes, self.n_hpo_term_genes, self.overlap_sig_hpo),
            set_labels=('HPO genes', 'GWAS genes'),
            set_colors=("silver", "lightsteelblue"), alpha=0.7)

        venn2_circles(subsets=(self.n_sig_genes, self.n_hpo_term_genes, self.overlap_sig_hpo),
                    linewidth=1)

    def show(self) -> None:
        """
        Show the venn diagram on screen.
        """
        self.__plot_venn_diagram()
        plt.show()

    def save(self, output_file) -> None:
        """
        Save the venn diagram to a file.

        :parameters
        -----------
        output_file - Path
            Location and name of the output file
        """
        self.__plot_venn_diagram()
        plt.savefig(output_file)
        plt.clf()


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


def save_fisher_results(file, fisher_table, odds_ratio, pval, precision, recall) -> None:
    """
    Save the results of a fisher's exact test to a txt file.

    :parameters
    -----------
    file - Path
        Output file name and location
    fisher_table - str
        2x2 contingency table used for the fisher's exact test
    odds_ratio - float
        Odds ratio of the fisher's exact test
    pval - float
        P value of the fisher's exact test
    """
    with open(file, 'w', encoding="utf-8") as file_handler:
        file_handler.write("2x2 contingency table:\n")
        file_handler.write(fisher_table)
        file_handler.write(f"\nprecision: {precision}, recall: {recall}\n")
        file_handler.write("\nFisher's exact test results:")
        file_handler.write(f"odds ratio: {odds_ratio}, pvalue: {pval}\n")



def print_fisher_results(fisher_table, odds_ratio, pval, precision, recall) -> None:
    """
    Print the results of a fisher's exact test to the screen

    :parameters
    -----------
    fisher_table - str
        2x2 contingency table used for the fisher's exact test
    odds_ratio - float
        Odds ratio of the fisher's exact test
    pval - float
        P value of the fisher's exact test
    """
    print("2x2 contingency table:\n")
    print(fisher_table)
    print(f"\nprecision: {precision}, recall: {recall}\n")
    print("\nFisher's exact test results:")
    print(f"odds ratio: {odds_ratio}, pvalue: {pval}\n")



def calculate_recall_precision(true_positives, false_positives, false_negatives) -> Tuple[float, float]:
    """
    Calculate the recall and precision.

    :parameters
    -----------
    true_positives - int
        Number of true positives (i.e. number of prioritized genes that are inside the HPO term gene list)
    false_positives - int
        Number of false positives (i.e. number of prioritized gene that are not inside the HPO term gene list )
    false_negatives - int
        Number of false negatives (i.e. number of genes that were not prioritized that are inside the HPO term gene list)

    :returns
    --------
    precision - float
        the precision (i.e. the proportion of prioritized genes in the gold standard set.)
    recall - float
        the recall (i.e. the proportion of genes in the gold standard set that were prioritized)
    """
    precision = np.round(true_positives / (true_positives + false_positives), 4)
    recall = np.round(true_positives / (true_positives + false_negatives), 4)

    return precision, recall


def main():
    """
    Run the entire program
    """
    arg_parse = ArgumentParser()

    config_file = arg_parse.get_argument("c")
    method = arg_parse.get_argument("m")
    output_dir = arg_parse.get_argument("o")

    # Save or plot mode
    save_mode = arg_parse.get_argument('s')
    mode= "save" if save_mode else "plot"

    cli_validator = CLIArgValidator()
    cli_validator.validate_input_file(config_file)
    cli_validator.check_arg_combination(output_dir, save_mode)

    if output_dir:
        make_out_dir(Path(output_dir))

    config = get_config(Path(config_file))

    methods = {"NetWAS": NetWAS, "PoPs": PoPs, "DEPICT": Depict,
                "Downstreamer": Downstreamer, "MAGMA":Magma}

    hpo_data = config["hpo_data"]
    hpo = HPO(database=hpo_data)
    fisher = FisherTest()

    method_instance = methods[method](hpo=hpo, fisher=fisher)

    for trait, info in config["traits"].items():
        print(f"Processing trait: {trait}")
        file = Path(info["file"])
        hpo_term = info["hpo_term"]
        method_data, genes = method_instance.read_data(file)

        _, overlap_genes, _ = method_instance.get_overlap(hpo.hpo_data, genes)

        overlap_method = method_instance.get_overlap_genes(method_data, overlap_genes)

        _, sig_genes = method_instance.filter_data(overlap_method)

        _, genes_hpo_term = hpo.get_data_hpo_term(hpo.hpo_data, hpo_term)

        fisher_data = fisher.create_fisher_table(overlap_genes, sig_genes, genes_hpo_term)

        true_positives, false_positives, false_negatives = fisher_data.iloc[1, 1], fisher_data.iloc[1, 0], fisher_data.iloc[0, 1]

        fisher_table = fisher_data.to_string()

        odds_ratio, pval = fisher.fishers_exact_test(fisher_data.iloc[0:2, 0:2].values)

        precision, recall = calculate_recall_precision(true_positives, false_positives, false_negatives)

        # Create venn diagram
        n_significant_genes = len(sig_genes)
        n_hpo_term_genes = len(genes_hpo_term)
        overlap_sig_hpo = fisher_data.iloc[1, 1]
        venn_diagram = VennDiagram(n_significant_genes, n_hpo_term_genes, overlap_sig_hpo)

        # Save results
        if mode == "save":
            venn_diagram.save(Path(output_dir) / (trait + "_venn.png"))
            save_fisher_results(Path(output_dir) / (trait + "_fisher_results.txt"),
             fisher_table, odds_ratio, pval, precision, recall)
        else: # Plot results
            venn_diagram.show()
            print_fisher_results(fisher_table, odds_ratio, pval, precision, recall)


if __name__ == "__main__":
    main()
