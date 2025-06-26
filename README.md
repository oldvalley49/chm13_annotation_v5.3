## Proposed Changes to the T2T-CHM13 Annotation

### Background
285 genes from the MANE gene annotation in GRCh38 are missing in the current CHM13 annotation. 

### Proposed Changes
1.  Updating gene names to their newest versions in MANE. 
A subset of genes in the current CHM13 annotation have updated names. In particular, some LOC genes have 
since then been given standard gene names. We replace their gene names and gene biotypes but keep the 
current gene coordinates in the CHM13 annotation. We replac ethe gene biotypes because in certain cases, 
gene synonyms are listed with different biotypes (most commonly protein-coding <-> pseudogene, but occasionally 
protein-coding <-> lncRNA).

    List of entries to remove: `changes/1_synonyms_remove.csv`

    List of entries to add: `changes/1_synonyms_add.csv`

2.  After the first step, there are still 107 MANE genes missing. The current CHM13 annotation is based on lifting over the RefSeq annotation from GRCh38 to CHM13. We also lifted over the MANE annotation to see if these missing genes can be mapped to CHM13. After mapping the MANE genes to CHM13, we looked at the coordinates 
of the 107 missing MANE genes to see if they overlap with any of the currently annotated genes. 

    There were 3 cases in which MANE genes exactly overlapped with a LOC gene currently annotated in CHM13. While they are not listed as synonyms in [HUGO](https://www.genenames.org/) or [NCBI](https://www.ncbi.nlm.nih.gov/), we reasoned that their sequences are similar enough to be replaced by the MANE genes. 

    List of entries to remove: `changes/2_exact_remove.csv`

    List of entries to add: `changes/2_exact_add.csv`

3. There were 7 cases in which MANE genes were not annotatated because a separate LOC gene had already been annotated in an overlappnig location. In this case,
we add the MANE genes and their mapped coordinates, and remove the LOC genes from the annotation. 

    List of entries to remove: `changes/3_standard_loc_remove.csv`

    List of entries to add: `changes/3_standard_loc_add.csv`

4. There were 4 cases in which a MANE genes were not annotated because a fusion gene had taken its place. In this case, we remove the fusion gene from the annotation and add the MANE gene. 

    List of entries to remove: `changes/4_fusion_remove.csv`

    List of entries to add: `changes/4_fusion_add.csv`

5. There were 36 cases in whcih MANE genes were not annotated because another standard gene (as opposed to LOC gene) was already annotated in an overlapping location. In this case, we replace them with the MANE genes only if the JHU gene is not in MANE. If not, we still add the MANE gene but keep the original gene as well. 

    List of entries to remove: `changes/5_standard_remove.csv`

    List of entries to add: `changes/5_standard_add.csv`

6. Finally, there were 71 cases in which MANE genes were not annotated because another gene in its gene family was already annotated in CHM13. In this case, we replace them with the MANE genes using liftoff coordinates. 

    List of entries to remove: `changes/6_family_remove.csv`
    
    List of entries to add: `changes/6_family_add.csv`