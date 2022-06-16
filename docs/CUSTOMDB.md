## Compiling Protein sequences for the custom database from NCBI, KEGG and other databases
This step is necessary to extend the scope of proteins that Prokka uses by default to annotate genomes. 
For that, I will prepare a list of synonyms for all enzymes of interest and download them from NCBI.
This database will be called custom database (custom_db.faa) in later steps.

Make a new directory and switch to this directory:
```bash
mkdir 01_customdb
cd 01_customdb
```

#### 1) Using KEGG API to retrieve enzyme synonym names

Prepare a tab separated file following the example [uniq_ec.tsv](../examples/01_customdb/uniq_ec.tsv).

Columns in this file should contain: unique enzyme ID, pathway, pathway step ID, enzyme name, and EC number. Later, some of those columns will be used to organize the download output files.
Note that the unique enzyme ID and pathway ID are provided by the user from previous knowledge of the pathway of interest. In the example file, unique enzyme ID is provided using the convention E01, E02 etc. while the pathway step ID is named according to the pathway number and the step at which the enzyme is working at (e.g., pathway 1 step 1 is 1.1). Any other naming convention can be used in place of this provided that the column order does not change.

Please be aware that trailing spaces might exist depending on how you generated the file (e.g. Windows OS). 

To check for trailing spaces do:

```bash
cat -v uniq_ec.tsv
```
If there are any the symbol ^M at the end of the line should appear. To remove this;

```bash
mv uniq_ec.tsv > temp_file.tsv
sed -e "s/\r//g" temp_file.tsv > uniq_ec.tsv
```

Now the file is free of trailing whitespaces.

After preparing that file, retrieve the synonyms from KEGG using their API.
Please note that any typo or extra character in the EC number (e.g. space) may cause the synonyms to not be returned from KEGG API.
```bash
# Retrieve synonyms from KEGG API
cut -f5 uniq_ec.tsv | while read line; do out=$(curl -s http://rest.kegg.jp/list/ec:$line); echo $line $out; done > ec_synonyms.txt

# Combine tables
paste uniq_ec.tsv <(cut -f3- -d' ' ec_synonyms.txt) > synonyms_table.tsv
```

#### 2) Preparing the list of synonyms for NCBI Edirect
Parsing the synonyms to write down one synonym per line
```bash
# This bash pipeline also remove "gene name", "incorrect" and "misleading" synonyms

perl -ne 'chomp; @fields=split("\t",$_); @syn=split(";",$fields[4]); unless(scalar(@syn)==0){foreach(@syn){print join("\t",@fields[0..3]),"\t$_\n"}}else{print "$_\t$fields[2]\n"};' <(cut -f1,3- synonyms_table.tsv) | sed -e 's/\t /\t/g' | grep -v "incorrect\|gene name\|misleading" > synonyms_per_line.tsv
```

For some enzymes that did not return synonyms because of any reason, *manually insert the enzyme names that you know in column 5*.

Now, the following command will create a new column and add new IDs for synonyms (first column). That will be used to name the fasta files when using Edirect.
```bash
cat synonyms_per_line.tsv | perl -ne '$line=sprintf("%03d",$.); @fields=split("\t",$_); $synid="S$line-$fields[0]-$fields[3]"; if($fields[3] eq "NA"){print "$synid\t",join("\t",@fields[0..3]),"\t$fields[2]\n"}else{print "$synid\t$_"}' > id_synonyms_per_line.tsv
```

#### 3) Manually curating the list
Look through the "id_synonyms_per_line.tsv" and check for potential problems. (eg.: too short names that can cause ambiguity)

The following command removes synonyms with less than 6 characters to avoid ambiguity when querying NCBI.
```bash
# This perl code writes the changes in the same file
perl -ne 'chomp; @fields=split("\t",$_); $fields[5] =~ tr/ //d; unless(scalar(split("",$fields[5]))<=5){print "$_\n"};' id_synonyms_per_line.tsv > tmp; mv tmp id_synonyms_per_line.tsv 
```

#### 4) Using a custom perl script to download proteins from NCBI Edirect API
The custom script is based on the following example application: [Sample Applications of the E-utilities - Entrez Programming Utilities Help - NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK25498/#chapter3.Application_3_Retrieving_large)

This following code will run the "bulk_edirect_custom.pl" script. This script is available [here](../scripts/bulk_edirect_custom.pl).

If you are on EVE, do not forget to load the modules.
```bash
# Loading module
module load foss/2019b Perl/5.30.0
```
To run the script: 

```bash
# Create a folder to store download fasta files
mkdir edirect_fasta
```

```bash
# Running script
echo "START: $(date)"; cat id_synonyms_per_line.tsv | while read line; do id=$(echo "$line" | cut -f1); reac=$(echo "$line" | cut -f6 ); perl ../../scripts/bulk_edirect_custom.pl "$reac" protein $id edirect_fasta/ >> log.txt 2>> err.txt; done; echo "  END  : $(date)";
```
Since it can take hours or even days depending on the size of your list, I recommend running that with help of another tool (e.g. "screen").

Do not try to run many instances in parallel. 
This may cause NCBI to black list your IP in which case the log.txt file from this step may contain "RESULTS: ERROR" output for your queries.


#### 5) Adding missing proteins to custom database through OrtSuite-mediated searching in KEGG or manual downloading from other databases 

This step is necessary if there are enzymes
that were not collected by Edirect in the previous step. Otherwise, you can skip this step and continue with the Edirect downloaded proteins to perform the later steps.

For example, you can download some proteins that did not get downloaded by Edirect from the above step or additional proteins that you want to retrieve from KEGG Orthology directly using their EC numbers or KO identifiers. For the latter, the workflow uses OrtSuite. 


Create a folder to store manually downloaded fasta files
```bash
mkdir manual_download_fasta/
```

1) Downloading proteins using OrtSuite

For this step to be executed OrtSuite must be installed as described [here](https://github.com/mdsufz/OrtSuite).

I recommend checking OrtSuite github to learn how to use those commands.
Note that you must be at the OrtSuite environment in conda if you followed the conda installation [here](https://github.com/mdsufz/OrtSuite#readme).
Example files for ecs.txt and kos.txt can be found in [OrtSuite GitHub](https://github.com/mdsufz/OrtSuite/tree/master/examples).

```bash
# Downloading protein sequences based on a list of EC numbers
download_kos -o manual_download_fasta/ -e ecs.txt > log_ecs.txt 2> err_ecs.txt

# Downloading protein sequences based on a list of KO numbers
download_kos -o manual_download_fasta/ -k kos.txt > log_kos.txt 2> err_kos.txt
```

2) Manually downloading proteins from other sources

Also, I manually downloaded a couple of proteins.

Manually search for proteins in various databases (eg.: Uniprot, NCBI and KEGG) and save them into FASTA files.
This step is important when the automated retrieval in the previous steps did not work for some of the desired proteins.

```bash
# Example
 01_ana_benzene_carboxylase.faa
 02_benzoyl-coa_bamD.faa
 02_benzoyl-coa_bamE.faa
 02_benzoyl-coa_bamF.faa
 02_benzoyl-coa_bamG.faa
 02_benzoyl-coa_bamH.faa
 02_benzoyl-coa+reductase+bami.faa
 04_uniprot-Nitric+oxide+dismutase+(putative).faa
```
