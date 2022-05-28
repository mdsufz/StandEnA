#!/usr/bin/python3
import sys
#import json

######
#	
#	USAGE:
#	standard_proteins.py reaction.txt.uniq reaction.txt
#
######


protein_reference_names = {}

file = sys.argv[1]
prokka_standardized_proteins = open(file,"r")
while True:
	l = prokka_standardized_proteins.readline()
	if not l: break
	else:
		standard_name,assigned_name = l.strip().split("\t")
		protein_reference_names[assigned_name] = standard_name


prokka_standardized_proteins.close()

#print(json.dumps(protein_reference_names, indent = 4))


finalTable = {}

file = sys.argv[2]
prokka_results = open(file,"r")
lines = prokka_results.readlines()#[1:] # remove comment to skip header if necessary

#print(len(lines))

for l in lines:
	fields = l.strip().split("\t")
	#print(fields[0],fields[7])
	if fields[7] in protein_reference_names.keys():
		if protein_reference_names[fields[7]] != "REMOVE":
			finalTable[l.strip()] = protein_reference_names[fields[7]]
#print(finalTable)

for k,v in finalTable.items():
		print(k,v,sep="\t")
