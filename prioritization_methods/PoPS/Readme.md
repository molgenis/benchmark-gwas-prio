# PoPS: Polygenic Priority Score 

## Description
* * *
PoPS is a gene prioritization method, a new method to identify the causal genes, that integrate GWAS summary statistics with gene expression, biological pathway, and predicted protein-protein interaction.
The PoPS method is described in detail at: 

Weeks, E. M. et al. Leveraging polygenic enrichments of gene features to predict genes underlying complex traits and diseases. medRxiv (2020).
https://www.medrxiv.org/content/10.1101/2020.09.08.20190561v1


## An overview of how we applied PoPS for gene prioritization
* * *
 

 
## Step 1: Applying MAGMA to compuet the gene-level z-scores

First, we applied MAGMA to compute gene-level z-scores from GWAS summary statistics and an LD reference panel. To compute z-scores we performed two steps of MAGMA: gene annotation, and gene analysis.  

1. MAGMA: gene annotation step

in this step the gene p-values will be computed based on the snp p-valuse. To perform this step two datasets is needed: ``` gene_loc.txt ``` which I downloaded it from MAGMA website, and ``` snp_loc.txt ``` which is GWAS summary statistics dowanleded from GWAS catalogue. Both of these files needs to be pre-processed first based on what MAGMA manual asked. These preprocessing has been performed in the notebook [MAGMA_Preproceccing](https://github.com/molgenis/benchmark-gwas-prio/tree/main/prioritization_methods/MAGMA)


2. MAGMA: gene analysis step

in this step  z-scores were computed....
to perform the gene analysis step I used the bim file (contain 3 files), and the filtered GWAS summary statistics for each trait, and the output of the previous step(gene annotaion).. 

## Step 2: Munge features

In this step using the ```script src/munge_feature_files.py``` provided in [PoPS repository](https://github.com/FinucaneLab/pops) we processed the raw feature files (gene expression data, biological 
pathways, and predicted PPI networks) into a more efficient format for downstream usage. 

To do this we need to download the raw feature files from [here](https://github.com/FinucaneLab/gene_features).
The downloaded files needs to be also preprocessed before running the method. For example, we prefixed every column with the filename. 

**We applied the method also in different ways**: 

1. we used the features of only one tisseu, the most related tissue to the disease, for gene prioritisation, eg. the raw features of human bone marrow for height trait, colon for Inflamatory bowel disease trait and prostate for prostate cancer. [hbm_raw_features](https://github.com/molgenis/benchmark-gwas-prio/blob/main/prioritization_methods/PoPS/hbn_raw_features.ipynb), [PrC_raw_features](https://github.com/molgenis/benchmark-gwas-prio/blob/main/prioritization_methods/PoPS/PrC_raw_features.ipynb), [IBD_raw_features](https://github.com/molgenis/benchmark-gwas-prio/blob/main/prioritization_methods/PoPS/IBD_raw_features.ipynb).


2. we cobmbined the features of two tissues and used for gene prioritisation. [combine_hbm_colon_rawfeatures](https://github.com/molgenis/benchmark-gwas-prio/blob/main/prioritization_methods/PoPS/Combine%20hbm_colon_rawfeatures.py).  
3. we coombined the features of all the tissues and we used the same large set of features for gene priorisitation of all thhree traits. [download_allfeatures.sh](https://github.com/molgenis/benchmark-gwas-prio/blob/main/prioritization_methods/PoPS/download_features.sh), [combine_hbm_colon_rawfeatures](https://github.com/molgenis/benchmark-gwas-prio/blob/main/prioritization_methods/PoPS/rename_file_contents.py) 
 
## Step 3: Run PoPS
 
Next, PoPS performed marginal feature selection by using the output of MAGMA to perform enrichment analysis for each gene feature separately. 
To nominate causal genes, PoPS then assigned a priority score to every protein coding gene according to these enrichments. 



   to be continued



