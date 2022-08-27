# NetWAS - network-wide association study

NetWas is a method to re-prioritize genes based on tissue-specific networks. It combines genes with nominally significant genome-wide association study (GWAS) P values and tissue-specific networks to identify disease-gene associations more accurately than GWAS alone. It provides a useful reprioritization of the genome in terms of phenotypic and functional association [[1]](#references).

webservice: https://hb.flatironinstitute.org/netwas 

## Getting Started
* * *

### Input of NetWAS
NetWAS requires as input a GWAS result file, with per-gene p-values. These gene p-values can be calculated using versatile gene-based association study (VEGAS), pseq or forge. During this study VEGAS was used to calculate the gene p-values. In the [`process_GWAS_data/`](process_GWAS_data/) folder information on how to install VEGAS on your system is located as well as a script which is able to prepare GWAS summary statistics files to be able to be used for VEGAS.

### Processing results of NetWAS
The following scripts are used to process the results produced by NetWAS:
1. parse_netwas_results.py
2. convert_gene_id_ensembl_id.R

The results of NetWAS need to be processed before they can be used for analysis. First of all NetWAS adds a header to the output files, as can be seen [here](#example-output-netwas), this header needs to removed to be able to analyse the data. This can be done using the [`parse_netwas_results.py`](parse_netwas_results.py) script, optionally it can also be used to filter out the genes based on netwas score and to extract only the gene symbols. 

To check how the python script works you can look at the help function:

```bash
python3 parse_netwas_results.py -h
```

The next step is to convert the gene symbols into ensembl gene IDs. This is necessary in order to compare the results of NetWAS with HPO data because it only contains ensembl gene IDs and no gene symbols. An R script was written to convert the gene symbols of the NetWAS results into ensembl gene IDs, nameley [convert_gene_id_ensembl_id.R](convert_gene_id_ensembl_id.R).

This R script requires a configuration file to be present in the same directory with the name: [config.yml](config.yml)

Example:

```yaml
default:
  traits:
    height: "path/to/height/data.txt"
    PrC: "path/to/prostate_cancer/data.txt"
    IBD: "path/to/IBD/data.txt"
  output_folder: "output/folder/"
```

Inside the tratis section are all the results of NetWAS sepcified for different traits. The `output_folder` specifies where the resulting files should be saved. 

## Example output NetWAS

<div align="left">
  <a href="https://humanbase.readthedocs.io/en/latest/netwas.html">
    <img src="../../images/netwas_example.png" alt="Logo" width="80%">
  </a>
</div>

## References

**[1]** Greene CS*, Krishnan A*, Wong AK*, Ricciotti E, Zelaya RA, Himmelstein DS, Zhang R, Hartmann BM, Zaslavsky E, Sealfon SC, Chasman DI, FitzGerald GA, Dolinski K, Grosser T, Troyanskaya OG. (2015). Understanding multicellular function and disease with human tissue-specific networks. Nature Genetics. [10.1038/ng.3259w](https://www.nature.com/articles/ng.3259).



