import gffutils
import pandas as pd

# original = gffutils.create_db(
#     "data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3",
#     dbfn = "data/original.db",
#     force=True,
#     merge_strategy="warning",
#     disable_infer_genes = False,
#     disable_infer_transcripts = False,
#     id_spec = {'gene' : 'ID', 'transcript' : 'ID'}
# )

# mapped = gffutils.create_db(
#     "data/mapped.gff_polished",
#     dbfn = "data/mapped.db",
#     force=True,
#     merge_strategy="warning",
#     disable_infer_genes = False,
#     disable_infer_transcripts = False,
#     id_spec = {'gene' : 'ID', 'transcript' : 'ID'}
# )

original = gffutils.FeatureDB("data/original.db")
mapped = gffutils.FeatureDB("data/mapped.db")

## edit synonyms

remove = pd.read_csv("changes/1_synonyms_remove.csv", index_col = 0)
add = pd.read_csv("changes/1_synonyms_add.csv", index_col = 0)

# removing them

for gene in original.features_of_type("gene"):
    gene_name = (
        gene.attributes.get("Name", [None])[0]
        or gene.attributes.get("gene_id", [None])[0]
        or gene.id
    )
    chrom = gene.seqid
    start = gene.start
    end = gene.end
    strand = gene.strand

    match = remove[
        (remove["gene"] == gene_name)
        & (remove["chromosome"] == chrom)
        & (remove["start"] == start)
        & (remove["end"] == end)
        & (remove["strand"] == strand)
    ]

    if not match.empty:
        original.delete(gene, children=True)
    else:
        print(f"Gene {gene_name} was not found")

## add genes
for _, row in add.iterrows():
    gene_name = row["gene"]
    chrom = row["chromosome"]
    start = row["start"]
    end = row["end"]
    strand = row["strand"]

    # find matching gene in external DB
    for gene in external_db.features_of_type("gene"):
        gname = (
            gene.attributes.get("Name", [None])[0]
            or gene.attributes.get("gene_id", [None])[0]
            or gene.id
        )
        if (
            gname == gene_name
            and gene.seqid == chrom
            and gene.start == start
            and gene.end == end
            and gene.strand == strand
        ):
            # Add gene itself if not already present
            if not db.contains(gene.id):
                db.update([gene])

            # Add all descendants (children of children etc.)
            for descendant in external_db.children(gene, level=None, order_by="start"):
                if not db.contains(descendant.id):
                    db.update([descendant])

            print(f"Added gene {gene_name} at {chrom}:{start}-{end} ({strand})")