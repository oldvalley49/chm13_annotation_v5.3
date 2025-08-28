import pyfastx
import pandas as pd
from mjol.gan import *
import os

chm13 = GAn(
    file_name = 'data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3',
    file_fmt = 'gff'
)
chm13.build_db()
chm13.save_as_gix("output/chm13_original.pkl")

mapped = GAn(
    file_name = 'output/mapped_reformatted.gff',
    file_fmt = 'gff',
)
mapped.build_db()
mapped.save_as_gix("output/mapped_original.pkl")

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

df = pd.read_csv("changes_paired/overlaps_5.csv", index_col = 0)
df['gene_add_protein_length'] = df.apply(lambda row: get_protein_length(row['gene_add'], mapped, mapped_protein), axis=1)
df['gene_remove_protein_length'] = df.apply(lambda row: get_protein_length(row['gene_remove'], chm13, chm13_protein), axis=1)
df.to_csv("changes_paired/overlaps_7.csv")

