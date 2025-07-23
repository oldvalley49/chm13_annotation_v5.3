import pandas as pd
import gffpandas.gffpandas as gffpd
import os
import numpy as np

# load JHU annotation

JHU = gffpd.read_gff3("data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3")
JHU_df = JHU.attributes_to_columns()


# mapping

mapped = gffpd.read_gff3("data/mapped.gff_polished")
mapped_df = mapped.attributes_to_columns()

# load changes
add = pd.read_csv("changes/1_synonyms_add.csv", index_col = 0)
remove = pd.read_csv("changes/1_synonyms_remove.csv", index_col = 0)


JHU_df = JHU_df.rename(columns = {"seq_id":'chromosome'})
JHU_df = JHU_df[JHU_df['type'] == 'gene']
remove = remove.merge(
    JHU_df[['gene_remove', 'start', 'end', 'strand', 'chromosome', 'ID']],
    on = ['gene_remove', 'start', 'end', 'strand', 'chromosome'],
    how = 'left'
)

remove.to_csv("changes/1_synonyms_remove.csv")

mapped_df = mapped_df.rename(columns = {"seq_id":'chromosome'})
mapped_df = mapped_df[mapped_df['type'] == 'gene']

add = add.merge(
    mapped_df[['gene_add', 'start', 'end', 'strand', 'chromosome', 'ID']],
    on = ['gene_add', 'start', 'end', 'strand', 'chromosome'],
    how='left'
)

add.to_csv("changes/1_synonyms_add.csv")