## Annotating genomes using Prokka with a custom database
In this part, we are going to annotate our genomes using Prokka
with the additional custom database created in the previous step.


#### Creating a work directory
Create a directory where Prokka results will be saved to.
```bash
mkdir 02_annotation
```

#### Creating the custom database
In the next step we combine the additional [downloaded proteins](CUSTOMDB.md) into a custom database.

```bash
# Example (make sure to check the extensions of the files so you can use wildcard)
cat 01_customdb/edirect_fasta/*.faa 01_customdb/manual_download_fasta/*.faa > 02_annotation/custom_db.faa
```

#### Testing custom database
To make test if the newly created database is flawless, 
we can simply run "makeblastdb" on it.

```
makeblastdb -dbtype prot -in custom_db.faa -out custom_db
```

If you get an error like "BLAST Database creation error", something might be wrong with your database.
In my case, I identified some problematic lines and manually removed those.

Example on how to identify problematic lines and to fix them:
```bash
## Be aware this may not fix your specific problem

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
# Create a directory to store the renamed mags
# Here I call it "short"
mkdir short

# Move to the folder where your genomes are
cd genomes

# This awk command does the trick of renaming the fasta headers
# awk is taking each fasta as input and outputing to the directory short
for i in *; do awk '/^>/{print ">contig" ++i; next}{print}' < $i > ../short/"short_"$i; done
```

#### Running Prokka on genomes (on EVE cluster)

The following for loop will submit a job on EVE cluster for each genome to be annotated.
```bash
# Define working directory
workdir=/path/to/02_annotation
# Define prokka submission script
subscript_prokka=/path/to/prokka_on_bioindicators_v2.sh

for i in *.fa; do qsub -N $i $subscript_prokka $workdir/rep_set/short/$i prokka_out/"out_$i" $i; done
```
The submission script (which has the commands used) is available [here](../scripts/prokka_sub_script.sh).

**Please note that the script contains personal data and paths in the server. That all must be replaced by your own. 


#### Compiling all results into a single file

The most important output for our further analysis is the ".tsv" file 
(read about Prokka output files [here](https://github.com/tseemann/prokka#output-files)).

Concatenate all your ".tsv" outputs together.
```bash
# Concatenate files while printing filenames to first column
awk '{print FILENAME "\t" $0}' /path/to/prokka_annotation/*/*.tsv > prokka_all.tsv
```

Optional. Formating genome names from results.
```bash
sed -ri -e 's/^out_short_//' -e 's/\/PROKKA_[0-9]+\.tsv//' prokka_all.tsv
sed -ri '1 s/\S+/bin_id/' prokka_all.tsv
```
