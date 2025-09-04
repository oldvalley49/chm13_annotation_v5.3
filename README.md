# T2T-CHM13 Gene Annotation v5.3

## Motivation

We recently projected genes from the latest MANE gene annotation (v1.4) on GRCh38 onto the T2T-CHM13 v2.0 assembly, using Liftoff. 285 MANE genes were successfully lifted over but are currently missing from the T2T-CHM13 gene annotation v5.2. **The goal of this v5.3 update is to add as many of these missing MANE genes as possible.**

TODO: how many of these 256 MANE genes were added? 101 genes (107 including copies).

## Method

```
gene_A <- new gene projected from MANE v1.4
gene_B <- old gene in v5.2 overlapping with gene_A

IF gene_A and gene_B are OVERLAPPING in MANE v1.4:
    THEN ADD gene_A

ELSE IF gene_A has a broken ORF (invalid start and/or stop, premature stop codon):
    THEN KEEP gene_B

ELSE:
	  IF gene_B not in MANE v1.4:
		    REPLACE gene_B with gene_A

	  ELSE:
		    IF gene_B has no valid ORFs AND/OR gene_A encodes a longer protein than gene_B:
                REPLACE gene_B with gene_A
```
## Results

### Contact
Should you have any questions/suggestions regarding the update, please feel free to either open a GitHub issue or contact Tomo Furutani (<tfuruta1@jh.edu>), Hayden Ji (<hji20@jh.edu>), or Celine Hoh (<choh1@jhu.edu>).
