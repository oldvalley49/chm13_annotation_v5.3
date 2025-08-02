## Changes for the T2T-CHM13 Annotation v5.3

### Background
To address the 285 genes from the MANE gene annotation in GRCh38 are missing in the current CHM13 annotation. 

### Proposed Changes

1. Update gene names to match the latest MANE versions

Some genes in the CHM13 annotation have outdated names. In particular, several LOC-designated genes have since been assigned standard gene names. We will be updating the gene names and gene biotypes to reflect current MANE nomenclature, while preserving the original CHM13 gene coordinates.

2. Following step 1, 107 MANE genes remain unaccounted for. The current CHM13 annotation was derived by lifting over RefSeq annotations from GRCh38 using LiftOff. We similarly lifted over the MANE annotation and examined whether these missing genes could be mapped onto CHM13.

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

### T2T-CHM13 Gene Biotype Statistics (v5.2 vs. v5.3)

| Gene Biotype              | Old Count | New Count |
|--------------------------|-----------|-----------|
| protein_coding           | 20,008    | 20,089    |
| lncRNA                   | 18,389    | 18,385    |
| pseudogene               | 16,018    | 15,979    |
| miRNA                    | 2,046     | 2,044     |
| transcribed_pseudogene   | 1,262     | 1,256     |
| snoRNA                   | 1,188     | 1,187     |
| rRNA                     | 982       | 982       |
| tRNA                     | 523       | 523       |
| V_segment                | 245       | 245       |
| V_segment_pseudogene     | 209       | 209       |
| snRNA                    | 192       | 192       |
| J_segment                | 79        | 79        |
| ncRNA                    | 49        | 49        |
| misc_RNA                 | 37        | 37        |
| C_region                 | 23        | 23        |
| antisense_RNA            | 19        | 19        |
| other                    | 13        | 13        |
| Y_RNA                    | 7         | 7         |
| J_segment_pseudogene     | 6         | 6         |
| C_region_pseudogene      | 5         | 5         |
| vault_RNA                | 4         | 4         |
| scRNA                    | 4         | 4         |
| telomerase_RNA           | 1         | 1         |
| ncRNA_pseudogene         | 1         | 1         |
| RNase_MRP_RNA            | 1         | 1         |
| RNase_P_RNA              | 1         | 1         |

In version 5.3, there are 41 genes from the MANE annotation missing. The list of missing genes can be found at `log/missing_MANE_genes.txt`

### Scripts
The series of scripts used to update the gene annotation can be found in `scripts/`, named in the order in which they were executed. 

### Log
The `log/` directory contains log files for every change made in the gene annotation. 

`log/log.csv` is a csv file containing list of overlaps from step 2. The last column contains specific action taken(`RENAME`, `ADD`, `REMOVE`, `KEEP AS IS`) and their reasoning. 

`log/entries_added.txt` contains all entries (rows) of the GFF file that were added. 

`log/entries_removed.txt` contains all entries (rows) of the GFF file that were removed. 

### Contact
Should you have any questions/suggestions regarding the update, please feel free to either open a GitHub issue or contact Tomo Furutani (<tfuruta1@jh.edu>), Hayden Ji (<hji20@jh.edu>), or Celine Hoh (<choh1@jhu.edu>). 


