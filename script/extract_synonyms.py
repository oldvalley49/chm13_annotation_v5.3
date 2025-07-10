import pandas as pd
import gffpandas.gffpandas as gffpd
import os
import numpy as np
os.chdir("/home/tfuruta1/CHM13_changes")

# load JHU annotation

JHU = gffpd.read_gff3("../MANE_CHM13/data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3")
JHU_df = JHU.attributes_to_columns()

synonyms_remove = pd.read_csv("changes/1_synonyms_remove.csv")
synonyms_add = pd.read_csv("changes/1_synonyms_remove.csv")

JHU_df_edit = JHU_df[]