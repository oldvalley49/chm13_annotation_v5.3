gffread -O -F --keep-exon-attrs --sort-by data/chromosome_order.lst output/chm13_edited.gff3 > output/chm13_cleaned.gff3
awk 'BEGIN{OFS="\t"} $3=="mRNA"{$3="transcript"} {print}' output/chm13_cleaned.gff3 > output/test.gff
