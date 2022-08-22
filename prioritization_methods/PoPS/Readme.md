# PoPS: Polygenic Priority Score 

## Description
* * *
PoPS is a gene prioritization method, a new method to identify the causal genes, that integrate GWAS summary statistics with gene expression, biological pathway, and predicted protein-protein interaction.
The PoPS method is described in detail at: 

Weeks, E. M. et al. Leveraging polygenic enrichments of gene features to predict genes underlying complex traits and diseases. medRxiv (2020).



## An overview of how we applied PoPS for gene prioritization
* * *
First, we applied MAGMA (ref) to compute gene-level z-scores from GWAS summary statistics with an LD reference panel. 
to apply Magma we need to filter GWASs based on what MAGMA manual asked. 

The following notebook are used to process the results produced by MAGMA:


Next, we applied pops for marginal feature selection by using the output of MAGMA to perform enrichment analysis for each gene feature separately.
to do this we need to download all the raw feature files (gene expression data, biological 
pathways, and predicted PPI networks) from PoPS repository.  
Each feature file must be a tab-separated file with a header for column names. 
The column names must be unique across all feature files and we prefixed every column with the filename.
 
Next, PoPS performed marginal feature selection by using the output of MAGMA to perform enrichment analysis for each gene feature separately. 
To nominate causal genes, PoPS then assigned a priority score to every protein coding gene according to these enrichments. 



   to be continued



