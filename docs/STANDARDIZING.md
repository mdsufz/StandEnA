## Generating the Reference File for enzymes used in the annotation and standardizing protein names in Prokka results

If you have many different pathways, 
I suggest doing this part for each different pathways.
That way, you will end up having less proteins at a time
and this will ease the process.
Since some steps are manual, too many proteins can be confusing.


Creating directory for this part:
```
mkdir ../../03_standardization
cd ../../03_standardization
```
Note that the working directory from the [previous step](ANNOTATION.md) is 02_annotation/short/.

#### 1) Subsetting data to work with one pathway at a time

Example. Working with pathway of interest "1".

Creating directory for pathway 1:
```bash
mkdir pw_1
cd pw_1
```

Saving unique enzyme main names and synonyms for pathway (in this example it is pathway 1. enzymes [0-9]):
```bash
grep -P "\t1\.\d\t" ../../01_customdb/id_synonyms_per_line.tsv | cut -f4,5,6 | cut -f1,3 | sort | uniq > pw_1.txt
```
Note that the enzyme list is derived from the file "id_synonyms_per_line.tsv" that was used to download protein sequences using Edirect API in [step 1](CUSTOMDB.md). For example, if the 2. pathway is to be retrieved, the above line should be updated to search for "\t2\.\d\t" and the output file should be named accordingly (pw_2.txt).  

Note that queries formation in later steps from pw_1.txt will give an error if the file contains names with "/". These must be replaced by another character (e.g., in place of / put _).

```bash
#Replace all "/" with "_"
mv pw_1.txt temp_file.txt
sed -r "s/[/]+/_/g" temp_file.txt > pw_1.txt

#Remove intermediate files
rm temp_file.txt
```

Since the OrtSuite-mediated KEGG API download and manual download steps are performed after Edirect download and are optional, if manual download steps are used to retrieve sequences that are not included within "id_synonyms_per_line.tsv", additional steps should be performed to account for these protein names. In the steps below, there are additional codes to be executed to add OrtSuite-mediated KEGG API downloaded proteins (from EC numbers) to the required files and directories. These steps can be skipped if there are no OrtSuite-mediated KEGG API downloaded proteins (from EC numbers) or modified by the user if there are other download methods used (e.g., OrtSuite-mediated KEGG API downloaded proteins from KO identifiers).


#### 2) Dividing pathways into separate files for each enzyme/protein and collecting them in the queries directory

Each pathway will have a "queries" directory of files containing the enzyme synonyms to be searched for in the Prokka annotation in later steps.

Creating directory for storing queries:
```bash
mkdir queries
```

Printing each collection of synonyms to a different file:
```bash 
cat pw_1.txt | while read -r l; do line=$l; col2=$(echo "$l" | cut -f2); name=$(echo "$l" | cut -f1 | tr ' ' '_'); echo $col2 | sed -e 's/(.*//' >> queries/$name.txt ; done
```

Removing duplicated synonyms:
```bash
for i in queries/*; do sort $i | uniq > queries/tmp; mv queries/tmp $i; done
```
##### Example query file formation for OrtSuite-mediated KEGG API downloaded proteins (from EC numbers)
To be able to form query files, the EC numbers in ecs.txt must be used to retrieve enzyme names and synonyms. The below code is a variation of the [step 1](CUSTOMDB.md) to demonstrate the customizability of the code depending on specific needs. Please refer back to step 1 for detailed explanations.  

From this file, the enzyme synonyms and standard names can be added to files in the queries folder:
```bash 
cat path/to/ecs.txt | while read line; do out=$(curl -s https://rest.kegg.jp/list/ec:$line); echo $line $out; done > ortsuite_ec_synonyms.txt
```
After the synonyms and standard names have been collected into ortsuite_ec_synonyms.txt, we advise you to manually create a file similar to [uniq_ec.tsv](../examples/01_customdb/uniq_ec.tsv) containing the unique enzyme ID, pathway, pathway step ID, enzyme name, and EC numbers. Note that the enzyme name is the first name retrieved in ortsuite_ec_synonyms.txt and the fields unique enzyme ID, pathway, pathway step ID are dependent on the uniq_ec.tsv naming convention. The example file can be found here: [ortsuite_uniq_ec.tsv](../examples/03_standardization/pw_1/ortsuite_uniq_ec.tsv)

Then, the steps for the creation of ortsuite_id_synonyms_per_line.tsv are followed from [step 1](CUSTOMDB.md):
```bash
paste ortsuite_uniq_ec.tsv <(cut -f3- -d' ' ortsuite_ec_synonyms.txt) > ortsuite_synonyms_table.tsv
perl -ne 'chomp; @fields=split("\t",$_); @syn=split(";",$fields[4]); unless(scalar(@syn)==0){foreach(@syn){print join("\t",@fields[0..3]),"\t$_\n"}}else{print "$_\t$fields[2]\n"};' <(cut -f1,3- ortsuite_synonyms_table.tsv) | sed -e 's/\t /\t/g' | grep -v "incorrect\|gene name\|misleading" > ortsuite_synonyms_per_line.tsv
cat ortsuite_synonyms_per_line.tsv | perl -ne '$line=sprintf("%03d",$.); @fields=split("\t",$_); $synid="S$line-$fields[0]-$fields[3]"; if($fields[3] eq "NA"){print "$synid\t",join("\t",@fields[0..3]),"\t$fields[2]\n"}else{print "$synid\t$_"}' > ortsuite_id_synonyms_per_line.tsv
perl -ne 'chomp; @fields=split("\t",$_); $fields[5] =~ tr/ //d; unless(scalar(split("",$fields[5]))<=5){print "$_\n"};' ortsuite_id_synonyms_per_line.tsv > tmp; mv tmp ortsuite_id_synonyms_per_line.tsv
```
From this file, queries can be added to the queries directory following the same steps for the id_synonyms_per_line.tsv file above (starting from 1) Subsetting data to work with one pathway at a time) by changing the input to ortsuite_id_synonyms_per_line.tsv. Note that the file names for the OrtSuite-mediated KEGG API downloaded proteins are advised to be distinguished from Edirect downloaded proteins in the query file via a naming convention (e.g., queries/ortsuite_$name.txt for the file names to include "ortsuite"). The same naming convention is advised to be used for the intermediate files (e.g., ortsuite_pw_1.txt) to prevent overwriting the files created for Edirect downloaded proteins.


#### 3) Collecting standard database identifiers about the enzyme names used during annotation from KEGG to generate a reference file
The goal of this step is to generate the file "kegg_info.txt" for the
given pathway. This file can be used as a reference while manually curating the
protein names during the presence absence matrix generation in the [last step](PRESABS.md).


Gathering unique EC numbers for the pathway:
```bash 
grep -P "\t1\.\d\t" ../../01_customdb/id_synonyms_per_line.tsv | cut -f4,5 | sort | uniq > unique_pw_ec.tsv
```
Note that if the 2. pathway is to be retrieved, the above line should be updated to search for "\t2.\d\t".

Collecting ECs and KOs from KEGG API:
```bash
cat unique_pw_ec.tsv | cut -f2 | while read l; do curl -s https://rest.kegg.jp/link/ko/ec:$l; done | sort -k1,2 | uniq | grep -v "^$" > pw_ec_kos.txt
```

Collecting KO definitions (protein names):
```bash 
cut -f2 pw_ec_kos.txt | while read l; do def=$(curl -s https://rest.kegg.jp/get/$l | grep NAME | cut -f3- -d " "); paste <(echo $l) <(echo $def); done > kos_def.txt
```

Collecting main EC name (enzyme name):
```bash
cut -f1 pw_ec_kos.txt | while read l; do def=$(curl -s https://rest.kegg.jp/list/$l | cut -f2 | cut -f1 -d ";"); paste <(echo $l) <(echo $def); done > ec_name.txt
```

Combining all in a single file:
```bash
paste ec_name.txt kos_def.txt > pw_1_kegg_info.txt
```

Cleaning intermediate files (optional):
```bash
rm pw_ec_kos.txt kos_def.txt ec_name.txt
```
##### Example reference file formation for OrtSuite-mediated KEGG API downloaded proteins (from EC numbers)

Collecting ECs and KOs from KEGG API:
```bash
cat ecs.txt | while read l; do curl -s https://rest.kegg.jp/link/ko/ec:$l; done | sort -k1,2 | uniq | grep -v "^$" > ortsuite_ec_kos.txt
```
After this step, ortsuite_ec_kos.txt file can be used in place of pw_ec_kos.txt in the above steps (3) Collecting standard database identifiers about the enzyme names used during annotation from KEGG to generate a reference file) to generate the reference file. Note that the output and input file names for each of the above steps must be changed to prevent overwriting the reference files generated for Edirect downloaded proteins listed in id_synonyms_per_line.tsv. The suggested naming convention for these files is: ortsuite_kos_def.txt, ortsuite_ec_name.txt, [ortsuite_pw_1_kegg_info.txt](../examples/03_standardization/pw_1/ortsuite_pw_1_kegg_info.txt).

#### 4) Performing queries of the Prokka annotation using files in queries directory and dumping results into files


Changing to queries directory:
```bash
mkdir results
cd queries
```

Note: manually remove queries with brackets "[]" (if there are any). To test this:
```bash
grep -lFe [ -lFe ] -lFe "(" -lFe ")" *.txt
```
If there are file contents with brackets, the user is advised to use this code to remove the brackets but **keep the original files for later reference**:
```bash
#This will put the files in a subdirectory called new and use these files for the rest of the steps
mkdir new
for i in *.txt; do cat $i | tr -d '[]()' > new/$i; done
#Change to new/ to execute below steps
cd new/
```

For each query file, query for terms in the complete results. This step connects the standard names generated from previous steps with the protein annotation files generated by Prokka in [step 2](ANNOTATION.md).
```bash
for i in *.txt; do grep -i -f $i path/to/02_annotation/short/prokka_all.tsv > path/to/results/result_$i; done_
```


Moving results to a folder with complete results:
```bash
cd path/to/results
mkdir complete
mv *.txt complete
```

Summarizing result files by removing duplicates (unique):
```bash
mkdir unique
cd unique
for i in ../complete/*.txt; do cut -f8 $i | sort | uniq > $i.uniq; done; mv ../complete/*.uniq .
```

Now, the files for standardization should be ready.

Open each one of the ".uniq" files and include a new first column.
In this column annotate the standard name to the protein name of the second column.
If the second column cell does not relate to your protein, add "REMOVE" (without brackets).

Example .uniq file:

![Example image](../img/example_standardization.png)

Note that, depending on the specific protein headers present in the custom database generated in [step 2](ANNOTATION.md), Prokka annotation step can produce relatively "clean" outputs. This can mean that the first column that you add might contain the same information outputted by Prokka on the second column. An example "clean" .uniq file image is shown below:

![Example image](../img/example_clean_output.png)


#### 5) Combining standard names to Prokka annotation results (standardization of Prokka annotation)

Moving to results directory (going back to 03_standardization/pw_1/results/):
```bash
cd ../
```

Creating directory to store standardized results:
```bash
mkdir standardized
```

Adding standardized results to last column for each enzyme:
```bash
cd complete
for i in *; do python3 ../../../../../scripts/add_standard_names.py "../unique/$i.uniq" "$i" >> ../standardized/results_pw_1.txt; done
```

Note: The add_standard_names.py script is available [here](../scripts/add_standard_names.py).
