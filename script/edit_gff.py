import pandas as pd
import gffpandas.gffpandas as gffpd
import os
import numpy as np
os.chdir("/home/tfuruta1/CHM13_changes")

# load JHU annotation

JHU = gffpd.read_gff3("../MANE_CHM13/data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3")
JHU_df = JHU.attributes_to_columns()


# load changes
add = pd.read_csv("changes/2_standard_loc_add.csv", index_col = 0)
remove = pd.read_csv("changes/2_standard_loc_remove.csv", index_col = 0)

def remove_genes(df, remove_df):
    # get position of genes
    gene_pos = np.flatnonzero(df['type'] == 'gene')
    block_starts = gene_pos
    block_ends = np.append(gene_pos[1:], len(df))

    gene_rows = df.iloc[block_starts].copy()
    gene_rows["merge_key"] = (
        gene_rows["gene"].astype(str) + "|" +
        gene_rows["seq_id"].astype(str) + "|" +
        gene_rows["start"].astype(str) + "|" +
        gene_rows["end"].astype(str) + "|" +
        gene_rows["strand"].astype(str)
    )

    remove_df = remove_df.copy()
    remove_df["merge_key"] = (
        remove_df["gene"].astype(str) + "|" +
        remove_df["chromosome"].astype(str) + "|" +
        remove_df["start"].astype(str) + "|" +
        remove_df["end"].astype(str) + "|" +
        remove_df["strand"].astype(str)
    )

    blocks_to_remove = gene_rows["merge_key"].isin(remove_df["merge_key"])

    rows_to_drop = []
    for start, end, remove in zip(block_starts, block_ends, blocks_to_remove):
        if remove:
            rows_to_drop.extend(df.iloc[start:end].index)
    df_removed = df.iloc[rows_to_drop]
    df_result = df.drop(rows_to_drop)
    return df_result, df_removed

test, test_removed = remove_genes(JHU_df, remove)

test_removed.to_csv("log/standard_loc_removed.csv")