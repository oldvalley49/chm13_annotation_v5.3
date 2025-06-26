## Proposed Changes to the T2T-CHM13 Annotation

### Background
285 genes from the MANE gene annotation in GRCh38 are missing in the current CHM13 annotation. 

### Porposed Changes
1. Updating gene names to their newest versions in MANE. 
A subset of genes in the current CHM13 annotation have updated names. In particular, some LOC genes have 
since then been given standard gene names. We replace their gene names and gene biotypes but keep the 
current gene coordinates in the CHM13 annotation. We replac ethe gene biotypes because in certain cases, 
gene synonyms are listed with different biotypes (most commonly protein-coding <-> pseudogene, but occasionally 
protein-coding <-> lncRNA). 
List of entries to remove: `changes/1_synonyms_remove.csv`
List of entries to add: `changes/1_synonyms_add.csv`

2. After the first step, there are still 107 MANE genes missing. The current CHM13 annotation is based on lifting over the RefSeq annotation from GRCh38 to CHM13. We also lifted over the MANE annotation to see if these missing genes can be mapped to CHM13. After mapping the MANE genes to CHM13, we looked at the coordinates 
of the 107 missing MANE genes to see if they overlap with any of the currently annotated genes. 

There were three cases in which MANE genes exactly overlapped with a LOC gene currently annotated in CHM13. While they are not listed as synonyms in [HUGO](https://www.genenames.org/) or NCBI(https://www.ncbi.nlm.nih.gov/), we reasoned that their sequences are similar enough to be replaced by the MANE genes. 

List of entries to remove: `changes/2_exact_remove.csv`
List of entries to add: `changes/2_exact_add.csv`

3. 
