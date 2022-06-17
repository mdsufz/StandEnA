# StandEnA: A customizable workflow to create a standardized presence/absence matrix of annotated proteins

## Introduction
This workflow was created to predict and annotate proteins 
from genomes and to build a standardized matrix of presence/absence from the annotated proteins.
The outcome of this workflow can be used for many purposes. For example, to infer the genetic potential 
of a given organism to perform a pathway of interest.

## Installation instructions
Clone this repository
```bash
git clone https://github.com/mdsufz/std_enzymes
```
Install Miniconda3
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
Create and activate conda environment
```bash
conda create -n std_enzymes python=3.6.13
```

Set Perl 5.22.0 default path for libraries
```bash
conda env config vars set PERL5LIB=$CONDA_PREFIX/lib/perl5/site_perl/5.22.0/ -n std_enzymes
```

Activate environment
```bash
conda activate std_enzymes
```

Install required packages inside the environment
```bash
conda install -c bioconda perl-lwp-simple prokka blast==2.9.0
```
## Dependencies
To manual download additional proteins, OrtSuite is required. 
Follow the installation steps for OrtSuite [here](https://github.com/mdsufz/OrtSuite/).

## System requirements
A typical desktop (Linux) computer is capable of performing this workflow.
Disk space can be the most limiting resource for the annotation step as each annotated genome produces ~2,5G of data. Therefore, it is recommended to have a fair ammount of free space depending on the number of genomes to be annotated.


## Workflow steps
1. [Compiling Protein sequences for the custom database from NCBI, KEGG and other databases](docs/CUSTOMDB.md)
2. [Generating a custom database and annotating genomes using Prokka with this custom database](docs/ANNOTATION.md)
3. [Generating the Reference File for enzymes used in the annotation and standardizing protein names in Prokka results](docs/STANDARDIZING.md)
4. [Generating matrix of standardized presence absence](docs/PRESABS.md)

## Author of this workflow
- Felipe Borim Corrêa
- https://www.ufz.en/index.php?de=43567
