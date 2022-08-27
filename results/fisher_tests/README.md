## Description 
* * *
To be able to access whether or not a gene prioritization method has succeeded in prioritizing relevant genes is to compare them to genes that are known to be associated with a relevent human phenotype ontology (HPO) term. HPO is a standardize vocabulary of phenotypic abnormalities in human disease[[1]](#references). There are over 13000 term each describing a phenotypical abnormality. Each of these terms have genes that are known to be involved with that abnormality.

One way to get an overview of how well a prioritization method prioritized genes is to take a relevant HPO term and check how many of the prioritzed genes overlap with the genes documented for that HPO term. The **Fisher’s exact test** can be used to assess whether this enrichment is statistically significant. In addition, the odd ratios can be used to determine the direction of this association.

There are two different directories that both can be used to perform fisher's exact test on the results of a gene prioritization method: [`multiple_tests`](multiple_tests) and [`single_test`](single_test). 

The [`multiple_tests`](multiple_tests) can be used to perform multiple fisher's exact test on a whole list of different HPO terms and [`single_test`](single_test) can be used to perform a fisher's exact test on a specific HPO term.

The multiple_tests should mainly be used to check if different gene prioritization methods get similar performance for a list of HPO terms. The single_test should be used to find how well a gene prioritization method prioritized genes from a GWAS trait for a relevant HPO term.

## Gene Prioritization Methods
* * *
Currently there are five different gene prioritzation methods supported:

1. NetWAS
2. PoPs
3. DEPICT
4. MAGMA
5. Downstreamer

## References
* * *
**[1]** Köhler S, Carmody L, Vasilevsky N, et al. Expansion of the Human Phenotype Ontology (HPO) knowledge base and resources. Nucleic Acids Res. 2019;47(D1):D1018-D1027. doi:10.1093/nar/gky1105