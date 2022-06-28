#!/bin/bash


# loading modules
module load Anaconda3

#####$ -N $finalname
#$ -l h_rt=6:00:00
#$ -l h_vmem=4G -pe smp 10-12

# request 10 GiB of scratch space
# this sets up a per-job dedicated storage space
# access via the $TMPDIR1 variable, see usage below
 
#$ -wd /work/$USER
#$ -l scratch=10G
 
# output files
#$ -o /gpfs1/data/msb/felipe/benzene/metagenomes/prokka_annotation/logs/$JOB_NAME-$JOB_ID.out
#$ -e /gpfs1/data/msb/felipe/benzene/metagenomes/prokka_annotation/logs/$JOB_NAME-$JOB_ID.err

conda activate /home/borimcor/.conda/envs/prokka

cp -r "/gpfs0/home/borimcor/.conda/envs/prokka/db" "$TMPDIR1/."
cp -r "/gpfs1/data/msb/felipe/benzene/metagenomes/prokka_annotation/custom_database/new_custom_db.faa" "$TMPDIR1/."



echo "started prokka"
date
prokka "$1" \
	--outdir "$TMPDIR1/$2" \
	--proteins "$TMPDIR1/new_custom_db.faa" \
	--cpus "${NSLOTS:-1}" \
	--dbdir "$TMPDIR1/db" \
	--norrna --notrna

# copy final results
cp -r "$TMPDIR1/$2" "/work/$USER/$2"

echo "end annotate"
date
