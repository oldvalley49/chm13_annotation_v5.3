import pandas as pd
import gffpandas.gffpandas as gffpd
import os
os.chdir("/home/tfuruta1/CHM13_changes")

# load JHU and mapped
JHU = gffpd.read_gff3("../MANE_CHM13/data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3")
JHU_df = JHU.attributes_to_columns()

mapped = gffpd.read_gff3("../MANE_CHM13/output/1_mapped.gff")
mapped_df = mapped.attributes_to_columns()

JHU_columns = set(JHU_df.columns)
mapped_columns = set(mapped_df.columns)

common = JHU_