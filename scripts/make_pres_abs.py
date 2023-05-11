#!/usr/bin/python3
import sys
import json
from collections import defaultdict

######
#	
#	USAGE:
#	make_pres_abs.py results.txt ids_to_names.tsv
#
######


dict_bins = {}
dict_proteins = defaultdict(list)

# Read file and save into dictionaries what enzyme is present in what bin
file = sys.argv[1]
file_standardized_results = open(file,"r")
while True:
	l = file_standardized_results.readline()
	if not l: break
	else:
		fields = l.strip().split("\t")
		bin_name = fields[0]
		pro_name = fields[8]

		dict_proteins[pro_name].append(bin_name)
		dict_bins[bin_name] = 0
file_standardized_results.close()


# Read file with ids to names to print IDs os proteins
dict_id_to_name = {}
file2 = sys.argv[2]
file_ref_ids = open(file2,"r")
while True:
	l = file_ref_ids.readline()
	#print(l)
	if not l: break
	else:
		fields = l.strip().split("\t")
		dict_id_to_name[fields[1]] = fields[0]
file_ref_ids.close()


#print(json.dumps(dict_id_to_name, indent = 4))

#quit()


# For each enzyme, check if it was found in the current bin or not
pres_abs_df_rows = defaultdict(list)

for enzyme,bin in dict_proteins.items():
	for bin_name in dict_bins.keys():
		if(bin_name in bin):
			pres_abs_df_rows[enzyme].append(1)
		else:
			pres_abs_df_rows[enzyme].append(0)

print('Specie', ';'.join(str(bin_name) for bin_name in dict_bins.keys()), sep=";")

for k,v in pres_abs_df_rows.items():
#	print(k, ';'.join(str(x) for x in v), sep=";")
	print(dict_id_to_name[k], ';'.join(str(x) for x in v), sep=";")
