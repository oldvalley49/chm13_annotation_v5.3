sed -E 's/\b(ID|Parent)=(gene-|rna-|exon-|cds-)/\1=/g' output/MANE_mapped_target_reformatted.gff3 > output/MANE_mapped_target_ready.gff3
