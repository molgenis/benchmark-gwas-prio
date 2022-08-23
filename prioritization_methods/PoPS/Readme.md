# PoPS: Polygenic Priority Score 

## Description
* * *
PoPS is a gene prioritization method, a new method to identify the causal genes, that integrate GWAS summary statistics with gene expression, biological pathway, and predicted protein-protein interaction.
The PoPS method is described in detail at: 

Weeks, E. M. et al. Leveraging polygenic enrichments of gene features to predict genes underlying complex traits and diseases. medRxiv (2020).
https://www.medrxiv.org/content/10.1101/2020.09.08.20190561v1


## An overview of how we applied PoPS for gene prioritization
* * *
 First, we applied MAGMA to compute gene-level z-scores from GWAS summary statistics and an LD reference panel. 
 To compute z-scores scores we performed two steps of MAGMA: gene annotation, and gene analysis.  
 
### Step one: Applying MAGMA to compuet the gene-level z-scores

1) MAGMA: gene annotation step
in this step the gene p-values will be computed based on the snp p-valuse.  For gene annotation I used two datasets: gene_loc.txt which I downloaded it from MAGMA website, and snp_loc.txt which is GWAS summary statistics dowanleded from GWAS catalogue. Both of these files needs to be pre-processed first based on what MAGMA manual asked. we only select the requested columns. The name of the columns and also the ordder of the columns should be based on the standards of MAGMA. These preprocessing has been performed in the notebook....

2) MAGMA: gene analysis step
in this step  z-scores were computed....
to perform the gene analysis step I used the bim file (contain 3 files), and the filtered GWAS summary statistics for each trait, and the output of the previous step(gene annotaion).. 

### Step 2: Munge features
Next, we applied pops for marginal feature selection by using the output of MAGMA to perform enrichment analysis for each gene feature separately.
to do this we need to download all the raw feature files (gene expression data, biological 
pathways, and predicted PPI networks) from PoPS repository.  
Each feature file must be a tab-separated file with a header for column names. 
The column names must be unique across all feature files and we prefixed every column with the filename.
 
 ### Step 3: Run PoPS
Next, PoPS performed marginal feature selection by using the output of MAGMA to perform enrichment analysis for each gene feature separately. 
To nominate causal genes, PoPS then assigned a priority score to every protein coding gene according to these enrichments. 



   to be continued


