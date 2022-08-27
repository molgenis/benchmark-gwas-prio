"""
Module that contains functionality to process data from
different prioritization methods to be able to perform fisher exact tests.
"""

from abc import ABC, abstractmethod
import pandas as pd
from scipy import stats


class PrioritizationMethod(ABC):
    """
    Base class for a prioritization method.
    """

    @abstractmethod
    def read_data(self, data):
        """
        Read in data from a CSV file.

        :parameters
        -----------
        data - Path
            File containing the data
        """

    @abstractmethod
    def filter_data(self, data, threshold):
        """
        Filter the data by only keeping the 'significant' genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        threshold - float
            Threshold to determine what significant is.
        """

    @abstractmethod
    def get_overlap_genes(self, data, genes):
        """
        Get the data that overlaps with a list of specified genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        genes - pd.Series
            List of gene IDs
        """

    def get_overlap(self, hpo_data, genes):
        """
        Get the genes overlapping with the HPO database.

        :parameters
        -----------
        hpo_data - pd.DataFrame
            HPO data inside a pandas dataframe
        genes - pd.Series
            Series of gene IDs

        :returns
        --------
        overlap_hpo - pd.DataFrame
            HPO data overlapping with the supplied genes
        overlap_genes - pd.Series
            Genes overlapping with the HPO data
        total_overlap - int
            Total number of overlapping genes
        """
        overlapping_genes_data = hpo_data[hpo_data.index.isin(genes)]
        overlapping_genes = overlapping_genes_data.index
        total_overlap = overlapping_genes.shape[0]

        # Only keep the genes that overlap with HPO
        overlap_genes = genes[genes.isin(overlapping_genes)]

        # Only keep releveant HPO data
        overlap_hpo = hpo_data[hpo_data.index.isin(overlapping_genes)]
        return overlap_hpo, overlap_genes, total_overlap


class NetWAS(PrioritizationMethod):
    """
    Subclass for the gene prioritization method NetWAS.
    """

    def __init__(self, hpo, fisher):
        self.hpo = hpo
        self.fisher = fisher

    def read_data(self, data):
        """
        Read in data from a CSV file.

        :parameters
        -----------
        data - Path
            File containing the data

        :returns
        --------
        netwas_data - pd.DataFrame
            Data in a data frame
        genes - pd.Series
            Gene IDs
        """
        netwas_data = pd.read_csv(data, sep=",")
        genes = netwas_data.ensemble_id
        return netwas_data, genes

    def get_overlap_genes(self, data, genes):
        """
        Get the data that overlaps with a list of specified genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        genes - pd.Series
            List of gene IDs

        :returns
        --------
        overlap_netwas - pd.DataFrame
            Data overlapping with specified genes
        """
        overlap_netwas = data[data.ensemble_id.isin(genes)]
        return overlap_netwas

    def filter_data(self, data, threshold=0.5):
        """
        Filter the data by only keeping the 'significant' genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        threshold - float
            Threshold to determine what significant is.

        :returns
        --------
        significant_netwas - pd.DataFrame
            Data containing only the significant genes
        significant_genes - pd.Series
            Gene IDs of the significant genes
        """
        significant_netwas = data[data.netwas_score > threshold]
        significant_genes = significant_netwas.ensemble_id
        return significant_netwas, significant_genes


class PoPs(PrioritizationMethod):
    """
    Subclass for the gene prioritization method PoPs.
    """

    def __init__(self, hpo, fisher):
        self.hpo = hpo
        self.fisher = fisher

    def read_data(self, data):
        """
        Read in data from a CSV file.

        :parameters
        -----------
        data - Path
            File containing the data

        :returns
        --------
        pops_data - pd.DataFrame
            Data in a data frame
        genes - pd.Series
            Gene IDs
        """
        pops_data = pd.read_csv(data, sep="\t")
        genes = pops_data["ENSGID"]
        return pops_data, genes

    def get_overlap_genes(self, data, genes):
        """
        Get the data that overlaps with a list of specified genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        genes - pd.Series
            List of gene IDs

        :returns
        --------
        overlap_pops - pd.DataFrame
            Data overlapping with specified genes
        """
        overlap_pops = data[data["ENSGID"].isin(genes)]
        return overlap_pops

    def filter_data(self, data, threshold=500):
        """
        Filter the data by only keeping the 'significant' genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        threshold - float
            Threshold to determine what significant is.

        :returns
        --------
        significant_pops - pd.DataFrame
            Data containing only the significant genes
        significant_genes - pd.Series
            Gene IDs of the significant genes
        """
        significant_pops = data.sort_values("PoPS_Score", ascending=False).iloc[0:threshold, :]
        significant_genes = significant_pops["ENSGID"]
        return significant_pops, significant_genes


class Depict(PrioritizationMethod):
    """
    Subclass for the gene prioritization method Depict
    """

    def __init__(self, hpo, fisher):
        self.hpo = hpo
        self.fisher = fisher

    def read_data(self, data):
        """
        Read in data from a CSV file.

        :parameters
        -----------
        data - Path
            File containing the data

        :returns
        --------
        depict_data - pd.DataFrame
            Data in a data frame
        genes - pd.Series
            Gene IDs
        """
        depict_data = pd.read_csv(data, sep="\t")
        depict_data.columns = depict_data.columns.str.rstrip()
        depict_data["Ensembl Gene ID"] = depict_data["Ensembl Gene ID"].str.rstrip()
        depict_data["zscores"] = stats.zscore(depict_data["Nominal P value"], nan_policy='omit')
        genes = depict_data["Ensembl Gene ID"]
        return depict_data, genes

    def get_overlap_genes(self, data, genes):
        """
        Get the data that overlaps with a list of specified genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        genes - pd.Series
            List of gene IDs

        :returns
        --------
        overlap_depict - pd.DataFrame
            Data overlapping with specified genes
        """
        overlap_depict = data[data["Ensembl Gene ID"].isin(genes)]
        return overlap_depict

    def filter_data(self, data, threshold = None):
        """
        Filter the data by only keeping the 'significant' genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        threshold - float
            Threshold to determine what significant is.

        :returns
        --------
        significant_depict - pd.DataFrame
            Data containing only the significant genes
        significant_genes - pd.Series
            Gene IDs of the significant genes
        """
        significant_depict = data[data["False discovery rate < 5%"] == "Yes"]
        significant_genes = significant_depict["Ensembl Gene ID"]
        return significant_depict, significant_genes


class Downstreamer(PrioritizationMethod):
    """
    Subclass for the gene prioritization method Downstreamer.
    """

    def __init__(self, hpo, fisher):
        self.hpo = hpo
        self.fisher = fisher

    def read_data(self, data):
        """
        Read in data from a CSV file.

        :parameters
        -----------
        data - Path
            File containing the data

        :returns
        --------
        downstreamer_data - pd.DataFrame
            Data in a data frame
        genes - pd.Series
            Gene IDs
        """
        downstreamer_data = pd.read_excel(data, "GenePrioritization")
        genes = downstreamer_data["Gene ID"]
        return downstreamer_data, genes

    def get_overlap_genes(self, data, genes):
        """
        Get the data that overlaps with a list of specified genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        genes - pd.Series
            List of gene IDs

        :returns
        --------
        overlap_downstreamer - pd.DataFrame
            Data overlapping with specified genes
        """
        overlap_downstreamer = data[data["Gene ID"].isin(genes)]
        return overlap_downstreamer

    def filter_data(self, data, threshold = None):
        """
        Filter the data by only keeping the 'significant' genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        threshold - float
            Threshold to determine what significant is.

        :returns
        --------
        significant_downstreamer - pd.DataFrame
            Data containing only the significant genes
        significant_genes - pd.Series
            Gene IDs of the significant genes
        """
        significant_downstreamer = data[data["FDR 5% significant"] == True]
        significant_genes = significant_downstreamer["Gene ID"]
        return significant_downstreamer, significant_genes


class Magma(PrioritizationMethod):
    """
    Subclass for the gene prioritization method Magma.
    """

    def __init__(self, hpo, fisher):
        self.hpo = hpo
        self.fisher = fisher

    def read_data(self, data):
        """
        Read in data from a CSV file.

        :parameters
        -----------
        data - Path
            File containing the data

        :returns
        --------
        magma_data - pd.DataFrame
            Data in a data frame
        genes - pd.Series
            Gene IDs
        """
        magma_data = pd.read_csv(data, sep='\s\s+', engine='python')
        genes = magma_data["GENE"]
        return magma_data, genes

    def get_overlap_genes(self, data, genes):
        """
        Get the data that overlaps with a list of specified genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        genes - pd.Series
            List of gene IDs

        :returns
        --------
        overlap_magma - pd.DataFrame
            Data overlapping with specified genes
        """
        overlap_magma = data[data["GENE"].isin(genes)]
        return overlap_magma

    def filter_data(self, data, threshold=1.084e-4):
        """
        Filter the data by only keeping the 'significant' genes.

        :parameters
        -----------
        data - pd.DataFrame
            Data
        threshold - float
            Threshold to determine what gene is significant.

        :returns
        --------
        significant_magma - pd.DataFrame
            Data containing only the significant genes
        significant_genes - pd.Series
            Gene IDs of the significant genes
        """
        significant_magma = data[data["P"] < threshold]
        significant_genes = significant_magma["GENE"]
        return significant_magma, significant_genes
