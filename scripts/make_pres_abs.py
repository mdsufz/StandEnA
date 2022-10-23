#!/usr/bin/python3
import sys
import json
from collections import defaultdict

######
#	
#	USAGE:
#	make_pres_abs.py results.txt ids_to_names.tsv prokka_all.tsv
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
		#print(bin_name)
		pro_name = fields[8]
		#print(pro_name)
		dict_proteins[pro_name].append(bin_name)
		dict_bins[bin_name] = 0
file_standardized_results.close()
#print("Dict_bins1", dict_bins.items())
#print("Dict_proteins1", dict_proteins.items())
#quit()

dict_bins_all = {}
# Read file and save into dictionaries all bins annotated by Prokka (including the ones that have none of the desired enzymes)
file1 = sys.argv[3]
with open(file1,"r") as file_all_results: 
	next(file_all_results)
	while True:
		l = file_all_results.readline()
		if not l: break
		else:
			fields = l.strip().split("\t")
			bin_name_all = fields[0]
			#print(bin_name)
			dict_bins_all[bin_name_all] = 1
#print(dict_bins_all.items())

#quit()

# Check whether there are bins not present in results but in Prokka annotation
for bin_all in dict_bins_all.keys():
	if bin_all not in dict_bins.keys():
		dict_bins_all[bin_all] = 0
#print("Dict_bins_all", dict_bins_all.items())

#quit()

# Read file with ids to names to print IDs of proteins
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


#print("Dict_to_id", json.dumps(dict_id_to_name, indent = 4))

#quit()

# Check whether there are enzymes not present in results but in the ids_to_names.txt
for enzyme in dict_id_to_name.keys():
	if enzyme not in dict_proteins.keys():
		dict_proteins[enzyme] = 0
#print("Dict_proteins", dict_proteins.items())

#quit()


# For each enzyme, check if it was found in the current bin or not
pres_abs_df_rows = defaultdict(list)

for enzyme,bin in dict_proteins.items():
	#print(enzyme, bin)
	if bin == 0:
		for bin_name in dict_bins_all.keys():
			pres_abs_df_rows[enzyme].append(0)
	else:
		for bin_name in dict_bins_all.keys():
			#print(bin_name)
			if(bin_name in bin):
				pres_abs_df_rows[enzyme].append(1)
			else:
				pres_abs_df_rows[enzyme].append(0)
#quit()

#print((str(bin_name) for bin_name in dict_bins_all.keys()), sep=";"))
#v = list(dict_bins_all.keys())
#print("Pres_abs_df", pres_abs_df_rows.items())
#print("Dict_id_to_name", dict_id_to_name.items())

print('Specie', ';'.join([str(bin_name) for bin_name in dict_bins_all.keys()]), sep=";")

#quit()

for k,v in pres_abs_df_rows.items():
	#print(k, ';'.join(str(x) for x in v), sep=";")
	print(dict_id_to_name[k], ';'.join(str(x) for x in v), sep=";")
