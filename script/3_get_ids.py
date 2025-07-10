import pandas as pd
import gffpandas.gffpandas as gffpd
import os
import numpy as np
os.chdir("/home/tfuruta1/CHM13_changes")

# load JHU annotation

JHU = gffpd.read_gff3("../MANE_CHM13/data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3")
JHU_df = JHU.attributes_to_columns()
JHU_df = JHU_df[JHU_df['type'] == 'gene']
JHU_df = JHU_df.rename(columns = {"seq_id":'chromosome', 'start': 'start_remove', 'end':'end_remove', 'strand':'strand_remove', 'chromosome':'chromosome_remove', 'ID': 'ID_remove'})


mapped = gffpd.read_gff3("output/MANE_mapped_target_reformatted.gff3")
mapped_df = mapped.attributes_to_columns()
mapped_df = mapped_df[mapped_df['type'] == 'gene']
mapped_df = mapped_df.rename(columns = {"seq_id":'chromosome', 'start': 'start_add', 'end':'end_add', 'strand':'strand_add', 'chromosome':'chromosome_add', 'ID':  'ID_add'})

# mapping

for file in os.listdir('changes_paired/'):
    fp = 'changes_paired/' + file
    df = pd.read_csv(fp, index_col = 0)
    df = df.merge(
        JHU_df[['start_remove', 'end_remove', 'strand_remove', 'chromosome', 'ID_remove']],
        on = ['start_remove', 'end_remove', 'strand_remove', 'chromosome'],
        how = 'left'
    )
    df = df.merge(
        mapped_df[['start_add', 'end_add', 'strand_add', 'chromosome', 'ID_add']],
        on = ['start_add', 'end_add', 'strand_add', 'chromosome'],
        how = 'left'
    )
    df.to_csv(fp)
