### activate mjol

from mjol.base import *
from mjol.gan import *
import pandas as pd
import os

os.chdir("/home/tfuruta1/CHM13_changes")

logs = list()
swaps_df  = pd.read_csv("changes_paired/1_swap_synonym.csv", index_col = 0)

# load mapped and CHM13
chm13 = GAn(
    filename = 'output/CHM13_noY.gff',
    format = 'gff'
)
mapped = GAn(
    filename = 'output/MANE_mapped_target_reformatted.gff',
    format = 'gff',
    features = ['gene', 'mRNA', 'exon', 'CDS']
)
chm13.build_db(n_threads=3)
mapped.build_db(n_threads=6)

chm13.save_as_gix("output/chm13_original.pkl")
mapped.save_as_gix("output/mapped_original.pkl")


for _, row in swaps_df.iterrows():
    try:
        old, new = chm13.solve_synonym(
            row['ID_remove'], 
            mapped, 
            row['ID_add'],
            [('ID', 'ID'), ('gene_name', 'gene') , ('dbxref', 'dbxref'), 
            ('description','description'), ('copy_num_ID','copy_num_ID'),
            ('gene_biotype', 'gene_biotype')],
            [('gene', 'gene')],
            exclude_attributes = ['product']
        )
        logs.append((old, new))
    except KeyError as e:
        print(f"{row['ID_remove']} wasn;t found")

with open("log/synonyms.txt", "w") as f:
    f.write("******************************************************************************************************************************\n")
    for log in logs:
        old, new = log
        f.write("Removed:\n")
        f.write(f'{old}\n')
        f.write("--------------------------------------------------------------------------------------------------------------------------------\n")
        f.write("Added:\n")
        f.write(f'{new}\n')
        f.write("******************************************************************************************************************************\n")
    
chm13.to_gff("CHM13_noY_4.gff")