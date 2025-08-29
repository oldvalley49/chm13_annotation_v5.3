import pyranges as pr
import gffpandas.gffpandas as gffpd

MANE = gffpd.read_gff3("data/MANE.GRCh38.v1.4.refseq_genomic_filtered.gff")
MANE_mapped = gffpd.read_gff3("output/1_mapped.gff_polished")
JHU = gffpd.read_gff3("data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3")

MANE = MANE.filter_feature_of_type(['gene'])
MANE_mapped = MANE_mapped.filter_feature_of_type(['gene'])
JHU = JHU.filter_feature_of_type(['gene'])

MANE_df = MANE.attributes_to_columns()
MANE_mapped_df = MANE_mapped.attributes_to_columns()
JHU_df = JHU.attributes_to_columns()

# see which MANE genes appear in JHU annotation (from RefSeq)
MANE_genes = set(MANE_df['gene'].unique())
MANE_mapped_genes = set(MANE_mapped_df['gene'].unique())
JHU_genes = set(JHU_df['gene'].unique())

# MANE genes not mapped to CHM13 via liftoff
unmapped_genes = MANE_genes - MANE_mapped_genes
# MANE genes not in JHU annotation
missing_genes = MANE_genes - JHU_genes
# missing genes that were successfully lifted over when MANE -> T2T
target_genes = MANE_mapped_genes & missing_genes

print("Number of MANE genes not mapped in JHU:", len(missing_genes))
print("Number of MANE genes not mapped via liftoff:", len(unmapped_genes))
print("Number of MANE genes not mapped via liftoff and missing in JHU:", len(unmapped_genes & missing_genes))
print("Number of Target genes:", len(target_genes))


# output missing genes
with open("output/missing_genes.txt", "w") as file:
    for gene in missing_genes:
        file.write(f"{gene}\n")

target_MANE_mapped = MANE_mapped.get_feature_by_attribute('gene', target_genes)
target_MANE_mapped.to_gff3("output/target_MANE_mapped.gff")

## find overlaps

target_MANE = pr.read_gff3("output/target_MANE_mapped.gff")
target_JHU = pr.read_gff3("data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3")
# merge all the transcripts
target_JHU = target_JHU[target_JHU.Feature == "gene"]
overlaps = target_MANE.join(target_JHU)
overlaps_df = overlaps.df

keep_cols = ["Chromosome", "gene", "Start", "End", "Strand", "gene_biotype", "gene_b", "Start_b", "End_b", "Strand_b",'gene_biotype_b']
overlaps_df_slim = overlaps_df[keep_cols]
overlaps_df_slim = overlaps_df_slim[overlaps_df_slim['Strand'] == overlaps_df_slim['Strand_b']]
rename_cols = ["chromosome", "gene_MANE", 'start_MANE', 'end_MANE', "strand_MANE", "biotype_MANE", "gene_JHU", "start_JHU", "end_JHU", "strand_JHU", "biotype_JHU"]
overlaps_df_slim.columns = rename_cols
overlaps_df_slim.to_csv("output/overlaps.csv")
