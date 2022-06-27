# Benchmarking GWAS prioritization methods
* * *

## Description
* * *


## Installation
* * *
This project requires both R and python dependencies.

### Python

#### Single install
The easiest way to install all the required packages is via conda or pip. How to install conda on your system can be found [here](https://docs.anaconda.com/anaconda/install/index.html).

To create a new environment which contains all the required packages plus the right version run the following code:

```bash
  conda env create -f install/environment.yml
```

This will create a new environment named `benchmark-gwas-prio` which can be used to run this repository.

or:

```bash
  pip install -r install/requirements.txt
```

> NOTE: the environment.yml and requirements.txt are located in the install/ directory [here](install/).

#### Multiple installs
An other option is to install each package seperately, either with conda or pip.

conda:
```bash
  conda install <PACKAGE>=<VERSION>
```

pip
```bash
  pip install <PACKAGE>==<VERSION>
```

> NOTE: make sure to use the correct versions, which are listed [here](#python-packages).

### R

To install packages in R use the following code:

```R
install.packages('<PACKAGE>')
```

> NOTE: all R dependencies are listed [here](#r-packages)


## Getting started
* * *



## Requirements
* * *
| Software                                     | Version  |
| -------------------------------------------- | :------: |
| [Python](https://www.python.org/)            | `3.9.7`  | 
| [R](https://www.r-project.org/)              | `4.1.2`  |
| [Bash](https://www.gnu.org/software/bash/)   | `5.1.4`  |


## Python Packages
* * *
| Package                                              | Version  |
| ---------------------------------------------------- | :------: |
| [numpy](https://numpy.org/)                          | `1.21.2` |
| [pandas](https://pandas.pydata.org/)                 | `1.3.3`  |
| [bokeh](https://bokeh.org/)                          | `2.3.3`  |
| [panel](https://panel.holoviz.org/)                  | `0.12.1` |
| [holoviews](https://holoviews.org/)                  | `1.14.6` |
| [hvplot](https://hvplot.holoviz.org/)                | `0.7.3`  |
| [scipy](https://scipy.org/)                          | `1.7.1`  |
| [jupyter](https://jupyter.org/)                      | `1.0.0`  |
| [statsmodel](https://www.statsmodels.org/)           | `0.12.2` |
| [pathlib](https://pathlib.readthedocs.io/en/pep428/) | `1.0.1`  |
| [yaml](https://pyyaml.org/)                          | `5.4.1`  |
| [colorcet](https://colorcet.holoviz.org/)            | `2.0.6 ` |

# R Packages
* * *
| Package                                               | Version  |
| ----------------------------------------------------- | :------: |
| [biomaRt](http://www.biomart.org/)                    | `4.1.2`  |
| [dplyr](https://dplyr.tidyverse.org/)                 | `4.1.2`  |


## Authors
* * *
| Name                                                        | Role           | Institute             |
| ------------------------------------------------------------| :------------: | :-------------------: |
| [Raana Roohanitaziani](mailto:r.roohanitaziani@st.hanze.nl) | Project member | Hanze University DSLS |
| [Pieter de Jong](mailto:p.w.j.de.jong@st.hanze.nl)          | Project member | Hanze University DSLS |
| [Michael Cen Feng](mailto:m.cen.feng@st.hanze.nl)           | Project member | Hanze University DSLS |
| [Stijn Arends](mailto:s.arends@st.hanze.nl)                 | Project member | Hanze University DSLS |


## Acknowledgements
* * *



## License
* * * 
This project contains a MIT [license](./LICENSE.md)
