### activate mjol

from mjol.base import *
from mjol.gan import *
from mjol.tools import *
import pandas as pd
import os

swaps_df  = pd.read_csv("changes_paired/1_swap_synonym.csv", index_col = 0)

# load mapped and CHM13
chm13 = GAn(
    file_name = 'data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3',
    file_fmt = 'gff'
)
chm13.build_db()
chm13.save_as_gix("output/chm13_original.pkl")

mapped = GAn(
    file_name = 'output/MANE_mapped_target_ready.gff3',
    file_fmt = 'gff',
)
mapped.build_db()
mapped.save_as_gix("output/mapped_original.pkl")

chm13 = load_from_gix("output/chm13_original.pkl")
mapped = load_from_gix("output/mapped_original.pkl")

logs = []
actions = []
for _, row in swaps_df.iterrows():
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

swaps_df['action'] = actions


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
    
swaps_df.to_csv("log/paired/synonyms.csv")
chm13.save_as_gix("output/chm13_1.pkl")

### standard loc
logs = list()
actions = list()
chm13 = load_from_gix("output/chm13_1.pkl")
mapped = load_from_gix("output/mapped_original.pkl")
swaps_df  = pd.read_csv("changes_paired/2_swap_standard_loc.csv", index_col = 0)

for _, row in swaps_df.iterrows():
    
    if ((row['ID_remove'] in chm13.lookup) and (row['ID_add'] not in chm13.lookup)):
        ### Replace them
        remove_uid = chm13.get_uid(row['ID_remove'])
        old = chm13.pop_feature(remove_uid, include_children=True)
        new_uid = mapped.get_uid(row['ID_add'])
        new_feature = mapped.get_feature(new_uid)
        new = chm13.add_feature(new_feature, include_children=True)
        logs.append((old, new))
        actions.append(f"DELETE {row['ID_remove']} and ADD {row['ID_add']}")
    elif (row['ID_remove'] in chm13.lookup):
        ### remove gene
        remove_uid = chm13.get_uid(row['ID_remove'])
        old = chm13.pop_feature(remove_uid, include_children=True)
        logs.append((old, "\n"))
        actions.append(f"DELETE {row['ID_remove']}")
    elif (row['ID_add'] not in chm13.lookup):
        ### add gene
        new_uid = mapped.get_uid(row['ID_add'])
        new_feature = mapped.get_feature(new_uid)
        new = chm13.add_feature(new_feature, include_children=True)
        logs.append(("\n", new))
        actions.append(f"ADD {row['ID_add']}")
    else:
        actions.append(f"ALREADY RESOLVED")

swaps_df['action'] = actions
with open("log/standard_loc.txt", "w") as f:
    f.write("******************************************************************************************************************************\n")
    for log in logs:
        old, new = log
        f.write("Removed:\n")
        f.write(f'{old}\n')
        f.write("--------------------------------------------------------------------------------------------------------------------------------\n")
        f.write("Added:\n")
        f.write(f'{new}\n')
        f.write("******************************************************************************************************************************\n")
swaps_df.to_csv("log/paired/standard_loc.csv")
chm13.save_as_gix("output/chm13_2.pkl")


### fusion
logs = list()
actions = list()
chm13 = load_from_gix("output/chm13_2.pkl")
mapped = load_from_gix("output/mapped_original.pkl")
swaps_df  = pd.read_csv("changes_paired/3_swap_fusion.csv", index_col = 0)

for _, row in swaps_df.iterrows():
    
    if ((row['ID_remove'] in chm13.lookup) and (row['ID_add'] not in chm13.lookup)):
        ### Replace them
        remove_uid = chm13.get_uid(row['ID_remove'])
        old = chm13.pop_feature(remove_uid, include_children=True)
        new_uid = mapped.get_uid(row['ID_add'])
        new_feature = mapped.get_feature(new_uid)
        new = chm13.add_feature(new_feature, include_children=True)
        logs.append((old, new))
        actions.append(f"DELETE {row['ID_remove']} and ADD {row['ID_add']}")
    elif (row['ID_remove'] in chm13.lookup):
        ### remove gene
        remove_uid = chm13.get_uid(row['ID_remove'])
        old = chm13.pop_feature(remove_uid, include_children=True)
        logs.append((old, "\n"))
        actions.append(f"DELETE {row['ID_remove']}")
    elif (row['ID_add'] not in chm13.lookup):
        ### add gene
        new_uid = mapped.get_uid(row['ID_add'])
        new_feature = mapped.get_feature(new_uid)
        new = chm13.add_feature(new_feature, include_children=True)
        logs.append(("\n", new))
        actions.append(f"ADD {row['ID_add']}")
    else:
        actions.append(f"ALREADY RESOLVED")

swaps_df['action'] = actions
with open("log/fusion.txt", "w") as f:
    f.write("******************************************************************************************************************************\n")
    for log in logs:
        old, new = log
        f.write("Removed:\n")
        f.write(f'{old}\n')
        f.write("--------------------------------------------------------------------------------------------------------------------------------\n")
        f.write("Added:\n")
        f.write(f'{new}\n')
        f.write("******************************************************************************************************************************\n")
swaps_df.to_csv("log/paired/fusion.csv")
chm13.save_as_gix("output/chm13_3.pkl")


### standard standard
logs = list()
actions = list()
chm13 = load_from_gix("output/chm13_3.pkl")
mapped = load_from_gix("output/mapped_original.pkl")
swaps_df  = pd.read_csv("changes_paired/4_swap_standard_standard.csv", index_col = 0)

for _, row in swaps_df.iterrows():
    
    if ((row['ID_remove'] in chm13.lookup) and (row['ID_add'] not in chm13.lookup)):
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
            actions.append(f"REMOVE {row['ID_remove']} and ADD {row['ID_add']} since {row['ID_remove']} has shorter protein sequence")
        else:
            actions.append(f"KEEP AS IS since both are in MANE, and {row['ID_remove']} has longer protein sequence")

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
    elif (row['ID_add'] not in chm13.lookup):
        ### add gene
        new_uid = mapped.get_uid(row['ID_add'])
        new_feature = mapped.get_feature(new_uid)
        new = chm13.add_feature(new_feature, include_children=True)
        logs.append(("\n", new))
        actions.append(f"ADD {row['ID_add']}, {row['ID_remove']} already removed")
    else:
        actions.append(f"ALREADY RESOLVED")

swaps_df['action'] = actions
with open("log/standard_standard.txt", "w") as f:
    f.write("******************************************************************************************************************************\n")
    for log in logs:
        old, new = log
        f.write("Removed:\n")
        f.write(f'{old}\n')
        f.write("--------------------------------------------------------------------------------------------------------------------------------\n")
        f.write("Added:\n")
        f.write(f'{new}\n')
        f.write("******************************************************************************************************************************\n")
swaps_df.to_csv("log/paired/standard_standard.csv")
chm13.save_as_gix("output/chm13_4.pkl")


### family
logs = list()
actions = list()
chm13 = load_from_gix("output/chm13_4.pkl")
mapped = load_from_gix("output/mapped_original.pkl")
swaps_df  = pd.read_csv("changes_paired/5_swap_family.csv", index_col = 0)

for _, row in swaps_df.iterrows():
    
    if ((row['ID_remove'] in chm13.lookup) and (row['ID_add'] not in chm13.lookup)):
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
            actions.append(f"REMOVE {row['ID_remove']} and ADD {row['ID_add']} since {row['ID_remove']} has shorter protein sequence")
        else:
            actions.append(f"KEEP AS IS since both are in MANE, and {row['ID_remove']} has longer protein sequence")

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
    elif (row['ID_add'] not in chm13.lookup):
        ### add gene
        new_uid = mapped.get_uid(row['ID_add'])
        new_feature = mapped.get_feature(new_uid)
        new = chm13.add_feature(new_feature, include_children=True)
        logs.append(("\n", new))
        actions.append(f"ADD {row['ID_add']}, {row['ID_remove']} already removed")
    else:
        actions.append(f"ALREADY RESOLVED")

swaps_df['action'] = actions
with open("log/family.txt", "w") as f:
    f.write("******************************************************************************************************************************\n")
    for log in logs:
        old, new = log
        f.write("Removed:\n")
        f.write(f'{old}\n')
        f.write("--------------------------------------------------------------------------------------------------------------------------------\n")
        f.write("Added:\n")
        f.write(f'{new}\n')
        f.write("******************************************************************************************************************************\n")
swaps_df.to_csv("log/paired/family.csv")
chm13.save_as_gix("output/chm13_5.pkl")


# sanity check
len(chm13.features)

# output to gff3
chm13.to_gff3("output/chm13_edited.gff3")