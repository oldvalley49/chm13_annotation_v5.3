import gffpandas.gffpandas as gffpd
import pandas as pd
import os

MANE = gffpd.read_gff3("data/MANE.GRCh38.v1.4.refseq_genomic.gff")
MANE_df = MANE.attributes_to_columns()
MANE_df = MANE_df[MANE_df['type'] == 'gene']


def genes_overlap(df_gff, gene1, gene2):
    df1 = df_gff[df_gff['gene'] == gene1]
    df2 = df_gff[df_gff['gene'] == gene2]

    for _, row1 in df1.iterrows():
        for _, row2 in df2.iterrows():
            # Check same chromosome
            if row1['seq_id'] != row2['seq_id']:
                continue
            # Check for overlap
            if not (row1['end'] < row2['start'] or row2['end'] < row1['start']):
                return True 
    return False

df = pd.read_csv("changes_paired/overlaps_synonyminfo.csv", index_col = 0)
df['overlapping_in_MANE'] = df.apply(lambda row: genes_overlap(MANE_df, row['gene_add'], row['gene_remove']), axis=1)
df.to_csv("changes_paired/overlaps_5.csv")


