## Proposed Changes for T2T-CHM13 Annotation v5.2

### Background
To address the 285 genes from the MANE gene annotation in GRCh38 are missing in the current CHM13 annotation. 

### Proposed Changes

1.  Update gene names to match the latest MANE versions

    Some genes in the CHM13 annotation have outdated names. In particular, several LOC-designated genes have since been assigned standard gene names. We will be updating the gene names and gene biotypes to reflect current MANE nomenclature, while preserving the original CHM13 gene coordinates.

Following step 1, 107 MANE genes remain unaccounted for. The current CHM13 annotation was derived by lifting over RefSeq annotations from GRCh38 using LiftOff. We similarly lifted over the MANE annotation and examined whether these missing genes could be mapped onto CHM13.

The main reason why many of these genes were not lifted over was because there was already another gene annotated in the location. Since Liftoff does not allow two genes to be mapped to an overlapping location, this caused a subset of genes to not be mapped at all to CHM13. When comparing coordinates of Liftoff mapped coordinates of currently missing genes versus the existing genes in CHM13, we discovered INSERT_NUMBER overlaps between their genomic coordinates. In many of these cases, we would like to prioritize the missing MANE gene as opposed to the currently annotated gene. For example, in many cases, the current CHM13 annotation has a non protein-coding gene where a protein coding gene could be annotated. 

To maximize the biological integrity of annotation, we resolve such conflicts using the following logic:

1. **Do the two overlapping genes overlap in the MANE annotation?**
   - ✅ **Yes** →  
     ➤ Keep **both** genes as overlapping in the CHM13 annotation as well.

   - ❌ **No** →
     2. **Are both overlapping genes present in the MANE annotation?**
        - ✅ **Yes** →  
          ➤ Keep the gene with the **longer protein sequence**.

        - ❌ **Only one is in MANE** →  
          ➤ Keep the gene that is in **MANE** and discard the other.





2.  Resolve conflicts between MANE and overlapping LOC genes

    10 MANE genes were missing because a separate LOC gene was already annotated at the same or overlapping location. Unlike 2 In these cases, we remove the LOC gene and replace it with the corresponding MANE gene using the lifted-over coordinates.

    Entries to remove: `changes/2_standard_loc_remove.csv`

    Entries to add: `changes/2_standard_loc_add.csv`

3. Resolve conflicts with fusion genes

    In 4 cases, MANE genes were absent because a fusion gene occupied the locus. We propose removing the fusion gene and replacing it with the corresponding MANE gene.

    Entries to remove: `changes/3_fusion_remove.csv`

    Entries to add: `changes/3_fusion_add.csv`

4. Resolve conflicts with non-LOC (standard) genes

    36 MANE genes were missing because a different standard gene (not a LOC gene) was already annotated in the same location.
    If the existing CHM13 gene is not included in MANE, we replace it with the MANE gene. If it is in MANE, we retain the CHM13 gene and still add the corresponding MANE gene.

    Entries to remove: `changes/4_standard_remove.csv`

    Entries to add: `changes/4_standard_add.csv`

5. Resolves conflicts within gene family

    71 MANE genes were missing due to the presence of another gene from the same gene family already annotated in CHM13. In these cases, we replace the existing gene with the corresponding MANE gene using liftover coordinates.

    Entries to remove: `changes/5_family_remove.csv`

    Entries to add: `changes/5_family_add.csv`