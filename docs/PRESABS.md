## Step 4 - Generating matrix of standardized presence absence

#### Step 4.1 - Combining all standardized Prokka results

Creating directory for this part and changing working directory to this:
```bash
mkdir 04_presabs
cd 04_presabs
```
Note that for [step 3.2.2](STANDARDIZATION.md) the working directory is at the subdirectory 03_standardization/pw_1/results/standardized/. The relative path from this point to the directory 04_presabs is:
```bash
mkdir ../../../../04_presabs
```

Combining all standardized results
```bash
cat ../03_standardization/pw_*/results/standardized/* > std_results_all.txt
```


#### Step 4.2 - Manually preparing file of protein/enzyme names to be used for generating the presence - absence matrix

Prepare a tab separated file (two columns) that contains the protein ID that you give to each of the protein standard names that you want to generate the matrix for. A tab-separated values file is a text format similar to comma-separated values files where, instead of a comma, a tab character is used to separate different fields. Please find more information on this file structure [here](https://en.wikipedia.org/wiki/Tab-separated_values).
Below is the example file ([ids_to_names.tsv](../examples/04_presabs/ids_to_names.tsv)):
```
CP1001	benzene dioxygenase, alpha subunit
CP1002	benzene dioxygenase, beta subunit
CP1003	benzene dioxygenase, ferredoxin component
CP1004	benzene dioxygenase, ferredoxin reductase component
```
Note that the protein IDs are dependent on the preference of the user. Here we suggested the usage of an ID convention of CP1001, CP1002 etc. Proteins to be used for the presence absence matrix is dependent on the user input but must match the names used in Prokka annotations and synonyms search performed using the query files in [step 3.2.1](STANDARDIZING.md). As a guideline, please check the your kegg_info.txt file for Edirect downloaded proteins (example file can be found under the name [pw_6_C_kegg_info.txt](../examples/03_standardization/pw_1/pw_6_C_kegg_info.txt)) and [ortsuite_pw_1_kegg_info.txt](../examples/03_standardization/pw_1/ortsuite_pw_1_kegg_info.txt) for proteins downloaded from KEGG using OrtSuite.generated in [step 3.1.3](STANDARDIZATION.md).

#### Step 4.3 - Running script to generate standardized presence - absence matrix
To prevent case-sensitivity as well as bracket differences while comparing the Prokka annotation with the standardized results, the Prokka annotation is recommended to be converted to lowercase and the brackets should be removed.
```bash
cat ../02_annotation/short/prokka_all.tsv |tr -d '[]()'| tr '[:upper:]' '[:lower:]' > prokka_all_updated.tsv
```

Using the ids_to_names.tsv file, run the script to generate the presence-absence matrix:
```bash
python3 ../../scripts/make_pres_abs.py std_results_all.txt ids_to_names.tsv prokka_all_updated.tsv > presence_absence.csv
```

Note: The make_pres_abs.py script is available [here](../scripts/make_pres_abs.py). If there is a split function error stating "expected 2 got 1" or "expected 2 got more", this is likely due to the lack of the required tab character or an additional tab character within a lines within .uniq files manually curated in [step 3.2.1](STANDARDIZING.md) which is propagated to the std_results_all.txt file. In this case, go back to the 03_standardization/results/unique/ directory files and manually fix these mistakes. Alternatively, run this code to look at the number of columns in each file (must be exactly 2):
```bash
cd ../03_standardization/pw_1/results/unique
for i in *.uniq; do awk -F'\t' '{print NF}' $i; echo $i; done
```
This code is an example for checking the number of columns separated by tabs in the .uniq files for pathway 1. To check the rest of the pathway files, change workng directory to 03_standardization/pw_N/. The output of the code will be the name of each file searched and the number of columns found in each line within that file. The output must be exactly 2 for each line to avoid errors.

Another possible error can be "KeyError" if the ids_to_names.tsv file generated in [step 4.2] does not match the standard names used in the standardization ([step 3.2.1](STANDARDIZATION.md)). In this case, change the names in the ids_to_names.tsv names file to match the standard names in the .uniq files.
