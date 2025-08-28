import gffpandas.gffpandas as gffpd


# MANE
MANE_mapped = gffpd.read_gff3("data/mapped.gff_polished")

# Remove prefixes from ID=... inside attributes
MANE_mapped.df['attributes'] = MANE_mapped.df['attributes'].str.replace(
    r'ID=(gene-|rna-|exon-|cds-)', 'ID=', regex=True
)

# Remove prefixes from Parent=... inside attributes
MANE_mapped.df['attributes'] = MANE_mapped.df['attributes'].str.replace(
    r'Parent=(gene-|rna-|exon-|cds-)', 'Parent=', regex=True
)

MANE_mapped.to_gff3("output/mapped_reformatted.gff")

