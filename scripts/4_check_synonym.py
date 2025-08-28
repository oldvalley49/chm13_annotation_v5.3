import sys
sys.path.append("utility")
import pandas as pd
from utility import *
import json

overlaps = pd.read_csv("changes_paired/overlaps.csv", index_col=0, dtype=str)

# compute overlap and overlap percentage
overlaps["overlap"] = overlaps.apply(lambda row: compute_overlap(int(row['start_add']), int(row['end_add']), int(row['start_remove']), int(row['end_remove'])), axis=1)
overlaps["overlap_percentage_add"] = overlaps.apply(lambda row: row['overlap']/(int(row['end_add']) - int(row['start_add'])), axis=1)
overlaps["overlap_percentage_remove"] = overlaps.apply(lambda row: row['overlap']/(int(row['end_remove']) - int(row['start_remove'])), axis=1)

# load dictinoary for synonym matching
with open("data/synonym_referencemap.json", "r") as f:
    synonym_map = json.load(f)
# NCBI database
database = pd.read_csv("data/Homo_sapiens.gene_info", sep='\t', dtype='str')

overlaps['synonym'] = overlaps.apply(lambda row: check_synonym(row['gene_add'], row['gene_remove'], synonym_map, database), axis=1)

overlaps.to_csv("changes_paired/overlaps_synonyminfo.csv")
