## Generating matrix of standardized presence absence

#### 1) Combining all standardized Prokka results

Creating directory for this part and changing working directory to this:
```bash
mkdir 04_presabs
cd 04_presabs
```
Note that the last step of [step 3](STANDARDIZATION.md) is at the subdirectory 03_standardization/pw_1/results/standardized/. The relative path from this point to the directory 04_presabs is:
```bash
mkdir ../../../../04_presabs
```

Combining all standardized results
```bash
cat ../03_standardization/pw_*/results/standardized/* > std_results_all.txt
```


#### 2) Manually preparing file of protein/enzyme names to be used for generating the matrix

##### a. Preparing index list of protein name to protein ID
Prepare a tab separated file (two columns) that contains the protein ID that you give to each of the protein standard names that you want to generate the matrix for. Below is the example file ([ids_to_names.tsv](../examples/04_presabs/ids_to_names.tsv)):
```
CP1001	benzene dioxygenase, alpha subunit
CP1002	benzene dioxygenase, beta subunit
CP1003	benzene dioxygenase, ferredoxin component
CP1004	benzene dioxygenase, ferredoxin reductase component
```
Note that the protein IDs are dependent on the preference of the user. Here we suggested the usage of an ID convention of CP1001, CP1002 etc. Proteins to be used for the presence absence matrix is dependent on the user input but must match the names used in Prokka annotations. As a guideline, please check the your kegg_info.txt file for Edirect downloaded proteins and [ortsuite_pw_1_kegg_info.txt](../examples/03_standardization/pw_1/ortsuite_pw_1_kegg_info.txt) for proteins downloaded from KEGG using OrtSuite.generated in [step 3](STANDARDIZATION.md). An example file can be found under the name [pw_6_C_kegg_info.txt](../examples/03_standardization/pw_1/pw_6_C_kegg_info.txt). 

##### b. Running script to generate matrix
Using the ids_to_names.tsv file, run the script to generate the presence-absence matrix:
```bash
python3 ../../scripts/make_pres_abs.py std_results_all.txt ids_to_names.tsv > presence_absence.csv
```

Note: The make_pres_abs.py script is available [here](../scripts/make_pres_abs.py).
