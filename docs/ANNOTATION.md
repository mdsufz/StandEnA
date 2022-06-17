## Generating a custom database and annotating genomes using Prokka with this custom database
In this part, we are going to annotate our genomes using Prokka
with the additional custom database to be created from the downloaded proteins in the [previous step](CUSTOMDB.md).


#### Creating a work directory
Create a directory where Prokka results will be saved to.
```bash
mkdir 02_annotation
```

#### Creating the custom database
In the next step we combine the additional [downloaded proteins](CUSTOMDB.md) into a custom database.

```bash
# Example (make sure to check the extensions of the files so you can use the wildcard)
cat 01_customdb/edirect_fasta/*.faa 01_customdb/manual_download_fasta/*.faa > 02_annotation/custom_db.faa
```
Note that if some files that have been manually downloaded in the previous step have different file extensions, they would not be added to the custom_db.faa with this code.

#### Testing the custom database
To test if the newly created database is "flawless", 
we can simply run "makeblastdb" on it.

```
makeblastdb -dbtype prot -in custom_db.faa -out custom_db
```

If you get an error like "BLAST Database creation error", something might be wrong with your database.
In my case, I identified some problematic lines and manually removed those.

Example on how to identify problematic lines and to fix them. Be aware that this may not fix your specific problem:
```bash
# Looking for "problematic" lines
sed -e  's/>/\n>/g' custom_db.faa | grep -P "\w>"
# Fixing those lines
sed -i  's/>/\n>/g' custom_db.faa
```

#### Shortening contig names
Prokka does not work when FASTA sequences have long headers (> 20 characters long). 
Therefore, it is necessary to rename the headers of 
the fasta files which will be used as input for annotation.

```bash
# Create a directory to store the renamed genomes
# Here I call it "short"
mkdir short

# Move to the folder where your genomes are
cd /path/to/genomes

# This awk command does the trick of renaming the fasta headers
# awk is taking each fasta as input and outputing to the directory short
for i in *; do awk '/^>/{print ">contig" ++i; next}{print}' < $i > ../short/"short_"$i; done
```

#### Running Prokka on genomes using the custom database

There are 2 alternative methods to run Prokka on genomes depending on your computational resources:

##### Running Prokka on EVE cluster

The following for loop will submit a job on EVE cluster for each genome to be annotated.
```bash
# Define working directory
workdir=/path/to/02_annotation
# Define prokka submission script
subscript_prokka=/path/to/prokka_on_bioindicators_v2.sh

for i in *.fa; do qsub -N $i $subscript_prokka $workdir/rep_set/short/$i prokka_out/"out_$i" $i; done
```
The submission script (which has the commands used) is available [here](../scripts/prokka_sub_script.sh).

**Please note that the script contains personal data and paths in the server. All of that must be replaced by your own information. 

##### Runing Prokka on local machine

Changing working directory to the directory containing the shortened genomes (from previous step):
```bash
cd /path/to/short
```
Note that this step can only be done after Prokka installation witin the std_enzymes conda environment as described [here](../README.md). std_enzymes conda environment must be activated as stated in the README.md file for this code to work.

Running Prokka for genomes:
```bash
for k in short/*.fa; do prokka $k --outdir prokka_out/"$k".prokka.output --prefix PROKKA_${k##*/} --proteins "custom_db.faa" --norrna --notrna --cpus 4 ; echo $k; done
```
Note that depending on your machine resources you can increase the cpu number to be used from --cpus option. See [Prokka](https://github.com/tseemann/prokka#readme) help page for detailed information on the flags used in the above code. 
This step puts all genome annotation files to the location 02_annotation/prokka_out/short.

#### Compiling all Prokka annotation results into a single file

The most important output for our further analysis is the ".tsv" file 
(read about Prokka output files [here](https://github.com/tseemann/prokka#output-files)).

Concatenate all your ".tsv" outputs together.
```bash
# Concatenate files while printing filenames to first column
awk '{print FILENAME "\t" $0}' /path/to/prokka_out/*/*.tsv > prokka_all.tsv
```

Optional. Formating genome names from results.
```bash
sed -ri -e 's/^out_short_//' -e 's/\/PROKKA_[0-9]+\.tsv//' prokka_all.tsv
sed -ri '1 s/\S+/bin_id/' prokka_all.tsv
```
