conda activate gene_annotation

agat_convert_sp_gxf2gxf.pl --gff data/chm13v2.0_RefSeq_Liftoff_v5.2_sorted.gff3

gffread -O -F --keep-exon-attrs data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3 > "test/chm13.sorted.gff"
