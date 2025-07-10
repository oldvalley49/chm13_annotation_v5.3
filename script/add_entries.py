import pandas as pd
import gffpandas.gffpandas as gffpd
import os
import numpy as np
os.chdir("/home/tfuruta1/CHM13_changes")

# load JHU annotation

JHU = gffpd.read_gff3("../MANE_CHM13/data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3")
JHU_df = JHU.attributes_to_columns()


# mapping

mapped = gffpd.read_gff3("data/mapped.gff_polished")
mapped_df = mapped.attributes_to_columns()


# entries to add
add_df = pd.read_csv("changes/2_standard_loc_add.csv", index_col = 0)

gene_loc = np.flatnonzero(mapped_df['type']=='gene')
block_starts = gene_loc
block_ends = np.append(gene_loc[1:], len(mapped_df))

gene_rows = mapped_df.iloc[block_starts].copy()
gene_rows["merge_key"] = (
    gene_rows["gene"].astype(str) + "|" +
    gene_rows["seq_id"].astype(str) + "|" +
    gene_rows["start"].astype(str) + "|" +
    gene_rows["end"].astype(str) + "|" +
    gene_rows["strand"].astype(str)
)

add_df = add_df.copy()
add_df["merge_key"] = (
    add_df["gene"].astype(str) + "|" +
    add_df["chromosome"].astype(str) + "|" +
    add_df["start"].astype(str) + "|" +
    add_df["end"].astype(str) + "|" +
    add_df["strand"].astype(str)
)

blocks_to_add = gene_rows['merge_key'].isin(add_df['merge_key'])

rows_to_add = []
for block_start, block_end, add in zip(block_starts, block_ends, blocks_to_add):
    if add:
        rows_to_add.extend(mapped_df.iloc[block_start:block_end].index)

features_to_add = mapped_df.iloc[rows_to_add]

assert(set(features_to_add['gene'].unique()) == set(add_df['gene']))
features_to_add.to_csv("log/standard_loc_added.csv")
combined = pd.concat([JHU_df, features_to_add], axis=0)

JHU.df = combined
JHU.to_gff3("test/JHU_new.gff3")
