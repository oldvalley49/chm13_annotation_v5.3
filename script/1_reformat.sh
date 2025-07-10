# MANE
sed 's/;Dbxref=/;dbxref=/g' output/MANE_mapped_target.gff > output/MANE_mapped_target_cleaned.gff
awk -F'\t' '($3=="lnc_RNA"){$3="mRNA"}1' OFS='\t' output/MANE_mapped_target_cleaned.gff > output/MANE_mapped_target_reformatted.gff
