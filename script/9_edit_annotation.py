### activate mjol
from mjol.base import *
from mjol.gan import *
from mjol.tools import *
import pandas as pd
import os

swaps_df  = pd.read_csv("changes_paired/overlaps_8.csv", index_col = 0)
chm13 = load_from_gix("output/chm13_original.pkl")
mapped = load_from_gix("output/mapped_original.pkl")
logs = []
actions = []

swaps_df_synonym = swaps_df[swaps_df['synonym']==True]
swaps_df_not_synonym = swaps_df[swaps_df['synonym']==False]

for _, row in swaps_df_synonym.iterrows():
    # update names if they are synonyms (keep transcript information, but update names)
    try:
        old, new = solve_synonym(
            chm13,
            chm13.get_uid(row['ID_remove']),
            mapped, 
            mapped.get_uid(row['ID_add']),
            {'gene':[('ID', 'ID'), ('gene_name', 'gene') , ('dbxref', 'dbxref'), 
                ('description','description'), ('copy_num_ID','copy_num_ID'),
                ('gene_biotype', 'gene_biotype'), ('gene', 'gene')], 
            'default':[('gene', 'gene')]},
            exclude_attributes = ['product']
        )
        logs.append((old, new))
        actions.append(f"RENAME {row['ID_remove']} to {row['ID_add']}")
    except KeyError as e:
        print(f"{row['ID_remove']} wasn;t found")

swaps_df_synonym['action'] = actions

actions = []
for _, row in swaps_df_not_synonym.iterrows():
    # synonym already added
    if row['gene_add'] in swaps_df_synonym.gene_add.values:
        actions.append(f"ALREADY RESOLVED via synonym update")
    # not resolved yet
    elif ((row['ID_remove'] in chm13.lookup) and (row['ID_add'] not in chm13.lookup)):
        ### Replace them
        remove_uid = chm13.get_uid(row['ID_remove'])
        new_uid = mapped.get_uid(row['ID_add'])
        new_feature = mapped.get_feature(new_uid)
        if row['overlapping_in_MANE']:
            new = chm13.add_feature(new_feature, include_children=True)
            old = "\n"
            logs.append((old, new))
            actions.append(f"KEEP {row['ID_remove']} and ADD {row['ID_add']} since overlapping in MANE")
        elif not row['gene_remove_in_MANE']:
            old = chm13.pop_feature(remove_uid, include_children=True)
            new = chm13.add_feature(new_feature, include_children=True)
            logs.append((old, new))
            actions.append(f"REMOVE {row['ID_remove']} and ADD {row['ID_add']} since {row['ID_remove']} not in MANE")
        elif row['gene_add_protein_length'] > row['gene_remove_protein_length']:
            old = chm13.pop_feature(remove_uid, include_children=True)
            new = chm13.add_feature(new_feature, include_children=True)
            logs.append((old, new))
            actions.append(f"REMOVE {row['ID_remove']} and ADD {row['ID_add']} since {row['ID_remove']} has strictly shorter protein sequence")
        else:
            actions.append(f"KEEP AS IS since both are in MANE, and {row['ID_remove']} has longer protein sequence")
    # gene to add is already added
    elif (row['ID_remove'] in chm13.lookup):
        ### remove gene
        remove_uid = chm13.get_uid(row['ID_remove'])
        if row['overlapping_in_MANE']:
            old = "\n"
            new = "\n"
            logs.append((old, new))
            actions.append(f"KEEP {row['ID_remove']} and ADD {row['ID_add']} since overlapping in MANE")
        else:
            old = chm13.pop_feature(remove_uid, include_children=True)
            logs.append((old, "\n"))
            actions.append(f"REMOVE {row['ID_remove']}, {row['ID_add']} already added")
    # gene to remove is already removed
    elif (row['ID_add'] not in chm13.lookup):
        ### add gene
        new_uid = mapped.get_uid(row['ID_add'])
        new_feature = mapped.get_feature(new_uid)
        new = chm13.add_feature(new_feature, include_children=True)
        logs.append(("\n", new))
        actions.append(f"ADD {row['ID_add']}, {row['ID_remove']} already removed")
    # already resolved
    else:
        actions.append(f"ALREADY RESOLVED")

swaps_df_not_synonym['action'] = actions
swaps_df_combined = pd.concat([swaps_df_synonym, swaps_df_not_synonym], axis=0, ignore_index=True)
swaps_df_combined.to_csv("log/log.csv")

with open("log/added.txt", "w") as f:
    f.write("******************************************************************************************************************************\n")
    for log in logs:
        old, new = log
        f.write(f'{new}\n')
        f.write("******************************************************************************************************************************\n")


with open("log/removed.txt", "w") as f:
    f.write("******************************************************************************************************************************\n")
    for log in logs:
        old, new = log
        f.write(f'{old}\n')
        f.write("******************************************************************************************************************************\n")

chm13.to_gff3("output/chm13_edited.gff3")