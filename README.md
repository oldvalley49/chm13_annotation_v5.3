## Changes for the T2T-CHM13 Annotation v5.3

### Background
To address the 285 genes from the MANE gene annotation in GRCh38 are missing in the current CHM13 annotation. 

### Proposed Changes

1.  Update gene names to match the latest MANE versions

    Some genes in the CHM13 annotation have outdated names. In particular, several LOC-designated genes have since been assigned standard gene names. We will be updating the gene names and gene biotypes to reflect current MANE nomenclature, while preserving the original CHM13 gene coordinates.

Following step 1, 107 MANE genes remain unaccounted for. The current CHM13 annotation was derived by lifting over RefSeq annotations from GRCh38 using LiftOff. We similarly lifted over the MANE annotation and examined whether these missing genes could be mapped onto CHM13.

The main reason why many of these genes were not lifted over was because there was already another gene annotated in the location. Since Liftoff does not allow two genes to be mapped to an overlapping location, this caused a subset of genes to not be mapped at all to CHM13. When comparing coordinates of Liftoff mapped coordinates of currently missing genes versus the existing genes in CHM13, we discovered 341 overlaps between their genomic coordinates. In many of these cases, we would like to prioritize the missing MANE gene as opposed to the currently annotated gene, such as when the current CHM13 annotation has a non protein-coding gene where a protein coding gene could be annotated. 

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

### Contact
Should you have any questions/suggestions, please feel free to either open a GitHub issue or contact Tomo Furutani<tfuruta1@jh.edu>, Hayden Ji<hji20.jh.edu>, or Celine Hoh<choh1@jhu.edu>. 


