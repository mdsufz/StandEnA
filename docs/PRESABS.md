## Calculating matrix os presence absence

#### 1) Combining all standardized prokka results

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


#### 2) Preparing files for calculating the matrix

##### a. Preparing index list of protein name to protein ID
Prepare a tab separated file (two columns) that contains the protein ID that you give to each of the protein standard names that you want to generate the matrix for. Below is the example file:
```
CP1001	benzene dioxygenase, alpha subunit
CP1002	benzene dioxygenase, beta subunit
CP1003	benzene dioxygenase, ferredoxin component
CP1004	benzene dioxygenase, ferredoxin reductase component
```

##### b. Running script to generate matrix
```bash
python3 ../../scripts/make_pres_abs.py std_results_all.txt ids_to_names.tsv > presence_absence.csv
```

Note: The make_pres_abs.py script is available [here](../scripts/make_pres_abs.py).
