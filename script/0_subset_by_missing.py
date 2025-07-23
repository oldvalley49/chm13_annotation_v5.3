import gffpandas.gffpandas as gffpd
import os

os.chdir("/home/tfuruta1/CHM13_changes")

MANE_mapped = gffpd.read_gff3("data/mapped.gff_polished")
CHM13 = gffpd.read_gff3("data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3")


with open("data/target_genes.txt", "r") as file:
    target_genes = {line.strip() for line in file}

chromosomes = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10',
               'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19',
               'chr20', 'chr21', 'chr22', 'chrX']

# because RBMY1B is in chrY
target_genes = target_genes - {'RBMY1B'}
MANE_mapped_subset = MANE_mapped.get_feature_by_attribute('gene', target_genes)
MANE_mapped_subset = MANE_mapped_subset.get_feature_by_attribute('seq_id', chromosomes)
CHM13_subset = CHM13.get_feature_by_attribute('seq_id', chromosomes)

MANE_mapped_subset.to_gff3("output/MANE_mapped_target.gff")
CHM13_subset.to_gff3("output/CHM13_noY.gff")

### Remember to replace RBMY1B manually, and to add back Y, and then sort them. 