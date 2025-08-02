import gffpandas.gffpandas as gffpd
import pandas as pd
import os

MANE = gffpd.read_gff3("data/MANE.GRCh38.v1.4.refseq_genomic.gff")
MANE_df = MANE.attributes_to_columns()
MANE_df = MANE_df[MANE_df['type'] == 'gene']

def gene_in_annotation(df_gff, gene):
    if df_gff[df_gff['gene']==gene].empty:
        return False
    return True

df = pd.read_csv("changes_paired/overlaps_7.csv", index_col = 0)
df['gene_remove_in_MANE'] = df.apply(lambda row: gene_in_annotation(MANE_df, row['gene_remove']), axis=1)
df.to_csv("changes_paired/overlaps_8.csv")