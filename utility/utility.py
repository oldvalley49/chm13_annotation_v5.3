import pandas as pd
import json
# function to check if one is synonym of other, gene order does not matter
def check_synonym(gene_A, gene_B, synonym_map, database):
    if gene_A not in synonym_map and gene_B not in synonym_map:
        print("both genes missing in HGNC, marking as not synonyms")
        return False
    if gene_A not in synonym_map or gene_B not in synonym_map:
        return False
    return gene_B in synonym_map[gene_A] or gene_A in synonym_map[gene_B]

# function to check the length of overlap (in base pairs)
def compute_overlap(start_A, end_A, start_B, end_B):
    start = max(start_A, start_B)
    end = min(end_A, end_B)
    return max(0, end-start)