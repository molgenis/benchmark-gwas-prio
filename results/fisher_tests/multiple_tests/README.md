## Description 
* * *

The scripts located in this directory can be used to perform fisher exact tests for a list of HPO terms([example](#example-hpo-list)) on the results of a prioritization method. 


## Getting Started
* * *
To be able to perform the fisher exact tests on the results of a gene prioritization method we need to run the [fisher_exact_test_prio_methods.py](fisher_exact_test_prio_methods.py) script. This script can process multiple results from different traits at the same time, which should be set in the configuration file.

Example:
```bash
python fisher_exact_test_prio_methods.py -c config.yaml -m NetWAS -o results/
```

> NOTE: use the `-h` to get the help message

### Requirements

* configuration file
    * Results of the prioritization method
    * HPO data
    * List of HPO terms
* Name of the prioritization method

### Config file

```yaml
traits:
  Height: "/path/to/height_results.txt"
  IBD: "/path/to/IBD_results.txt"
  PrC: "/path/to/prstcan_results.txt"

hpo_data: "/path/to/hpo_database.txt.gz"
hpo_info: "/path/to/hpo_list.csv
```

### Example HPO list

```csv
GWAS trait,Related HPO term,HPO ID
Body mass index,Abnormality of body mass index,HP:0045081
Height,Abnormality of body height,HP:0000002
Inflammatory bowel disease,increased inflamatory response,HP:0012649
Coeliac disease,increased inflamatory response,HP:0012649
Diastolic blood pressure,Abnormal systemic blood pressure,HP:0030972
Systolic blood pressure,Abnormal systemic blood pressure,HP:0030972
Pulse pressure,Abnormal systemic blood pressure,HP:0030972
Coronary artery disease,Abnormality of the cardiovascular system,HP:0001626
```
