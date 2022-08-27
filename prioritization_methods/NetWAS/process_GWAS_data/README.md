# Processing GWAS data


## Description
* * *
These scripts are designed to process GWAS data to be able to run the Versatile Gene-based Association Study (VEGAS2) software [[1]](#refrences). The GWAS summary statistics are required to be processed with VEGAS to be able to run NetWAS on the data. This is because NetWAS requires p-value per gene level data instead of the original p-value per SNP data. 

In order to run VEGAS the GWAS summary statistics must only contain two columns: SNP id and p-value, in a tab seperated file that does not contain any NaN values or a header.

e.q.:
```bash
rs1004739   0.00341
rs2898687   0.005083
rs7162781   0.6343
rs2905794   0.9469
rs1801052   0.9469
rs1013948   0.2093
rs2905877   0.955
rs12602834  0.9144
rs1129506   0.9284
rs7503263   0.4798
```

The purpose of these modules is to take any GWAS summary statistics file and to process it in such a way that it can be used to run VEGAS.

## Installation & Usage of VEGAS
* * *

How to install VEGAS2 and which dependencies are described are described in their [user manual](https://vegas2.qimrberghofer.edu.au/VEGAS2usermanual.pdf). An example of how to use VEGAS2 is described in one of their [tutorials](https://vegas2.qimrberghofer.edu.au/vegas2version2.tutorial.pdf). 

The actual executable (perl script) can be found [here](https://vegas2.qimrberghofer.edu.au/vegas2v2).

## Getting Started
* * *
As mentioned before these scripts can only be used to prepare the data for VEGAS and not for actually running the VEGAS software. 

The [`process_GWAS_data.py`](process_GWAS_data.py) script is the script which processes the data and puts it into the correct format. This script requires a configuration file to be located in the same directory with the name [`config.yaml`](config.yaml).

The [`validate_config.py`](validate_config.py) script is an util script which checks if the configuration file is correct. 

### Config File
* * *
The configuration file contains information about the different traits and were the output should be stored. Each trait has its own section and in that section the associated GWAS summary statistics file and optionally the names of the SNP and p-value columns. 

The user can set the names of the SNP and p-value columns to indicate which columns the program should use. However, the use could also let the program figure it out by setting `None` as a value. If the program sees a `None` value it will then look at the available column names and try to quess which columns most likely contains the SNP ids and the p values. 

Example of a config file:
```yaml
traits:
  PrC:
    file: "/path/to/prostate_cancer_gwas.txt"
    columns: {snp: "SNP", pval: "Pvalue"}
  IBD: 
    file: "/path/to/IBD_gwas.txt"
    columns: {snp: None, pval: None}
  height:
    file: "/path/to/height_gwas.txt"
    columns: {snp: SNP, pval: P}

output: "path/to/output/dir/"
```

## Refrences
* * *
**[1]** Mishra	A,	Macgregor	S.	VEGAS2:	Sobware	for	More	Flexible Gene-Based	Tes>ng.	Twin Res	Hum	Genet.	2015	Feb;18(1):86-91.	doi: [10.1017/thg.2014.79](https://europepmc.org/article/MED/25518859). Epub	2014	Dec	18.	Pubmed	ID:	25518859


