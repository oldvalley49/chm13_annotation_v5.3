## Proposed Changes to the T2T-CHM13 Annotation

### Background
To address the 285 genes from the MANE gene annotation in GRCh38 are missing in the current CHM13 annotation. 

### Proposed Changes

1.  Update gene names to match the latest MANE versions

    Some genes in the CHM13 annotation have outdated names. In particular, several LOC-designated genes have since been assigned standard gene names. We propose updating the gene names and gene biotypes to reflect current MANE nomenclature, while preserving the original CHM13 gene coordinates.
    We also update gene biotypes because gene synonyms can differ in biotype (commonly between protein-coding and pseudogene, or occasionally protein-coding and lncRNA).

    Entries to remove: `changes/1_synonyms_remove.csv`

    Entries to add: `changes/1_synonyms_add.csv`

Following step 1, 107 MANE genes remain unaccounted for. The current CHM13 annotation was derived by lifting over RefSeq annotations from GRCh38. We similarly lifted over the MANE annotation and examined whether these missing genes could be mapped onto CHM13.

2.  Resolve conflicts between MANE and overlapping LOC genes

    10 MANE genes were missing because a separate LOC gene was already annotated at the same or overlapping location. Unlike 2 In these cases, we remove the LOC gene and replace it with the corresponding MANE gene using the lifted-over coordinates.

    Entries to remove: `changes/2_standard_loc_remove.csv`

    Entries to add: `changes/2_standard_loc_add.csv`

3. Resolve conflicts with fusion genes

    In 4 cases, MANE genes were absent because a fusion gene occupied the locus. We propose removing the fusion gene and replacing it with the corresponding MANE gene.

    Entries to remove: `changes/4_fusion_remove.csv`

    Entries to add: `changes/4_fusion_add.csv`

4. Resolve conflicts with non-LOC (standard) genes

    36 MANE genes were missing because a different standard gene (not a LOC gene) was already annotated in the same location.
    If the existing CHM13 gene is not included in MANE, we replace it with the MANE gene. If it is in MANE, we retain the CHM13 gene and still add the corresponding MANE gene.

    Entries to remove: `changes/5_standard_remove.csv`

    Entries to add: `changes/5_standard_add.csv`

5. Resolves conflicts within gene family

    71 MANE genes were missing due to the presence of another gene from the same gene family already annotated in CHM13. In these cases, we replace the existing gene with the corresponding MANE gene using liftover coordinates.

    Entries to remove: `changes/6_family_remove.csv`

    Entries to add: `changes/6_family_add.csv`