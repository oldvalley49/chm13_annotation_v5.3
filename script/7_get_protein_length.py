import pyfastx
import pandas as pd
from mjol.gan import *
import os

chm13 = load_from_gix("output/chm13_original.pkl")
mapped = load_from_gix("output/mapped_original.pkl")
chm13_protein = pyfastx.Fasta('data/chm13_protein.fa')
mapped_protein = pyfastx.Fasta('data/mapped_protein.fa')

def get_protein_length(gene_id, annotation, fasta):
    gene_uid = annotation.get_uid(gene_id)
    gene_obj = annotation.get_feature(gene_uid)
    max_protein_len = 0
    for child in gene_obj.children:
        try:
            max_protein_len = max(max_protein_len, len(fasta[child.aid]))
        except KeyError as e:
            continue
    return max_protein_len

for file in os.listdir('changes_paired/'):
    fp = 'changes_paired/' + file
    df = pd.read_csv(fp, index_col = 0)
    df['gene_add_protein_length'] = df.apply(lambda row: get_protein_length(row['gene_add'], mapped, mapped_protein), axis=1)
    df['gene_remove_protein_length'] = df.apply(lambda row: get_protein_length(row['gene_remove'], chm13, chm13_protein), axis=1)
    df.to_csv(fp)
