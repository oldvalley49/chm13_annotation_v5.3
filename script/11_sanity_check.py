import gffpandas.gffpandas as gffpd


# MANE
MANE = gffpd.read_gff3("data/MANE.GRCh38.v1.4.refseq_genomic_filtered.gff")
MANE = MANE.filter_feature_of_type(['gene'])
MANE_df = MANE.attributes_to_columns()
MANE_genes = set(MANE_df['gene'].unique())

# new CHM13

CHM13 = gffpd.read_gff3("output/chm13_edited.gff3")
CHM13 = CHM13.filter_feature_of_type(['gene'])
CHM13_df = CHM13.attributes_to_columns()
CHM13_genes = set(CHM13_df['gene'].unique())

# old CHM13
CHM13_old = gffpd.read_gff3("data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3")
CHM13_old = CHM13_old.filter_feature_of_type(['gene'])
CHM13_old_df = CHM13_old.attributes_to_columns()
CHM13_old_genes = set(CHM13_old_df['gene'].unique())

missing_genes = MANE_genes - CHM13_genes

missing_genes_old = MANE_genes - CHM13_old_genes

print(f"missing genes: {len(missing_genes)}")

with open("log/missing_MANE_genes.txt", "w") as f:
    for gene in missing_genes:
        f.write(f"{gene}\n")