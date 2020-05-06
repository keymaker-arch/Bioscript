import re


# extract gene id, identity, evalue and bitscore from blast
# take in one line in blast output, and return each value for following screening
def blast_line_extract4(blast_line):
    pattern_blast_line = '^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$'
    match = re.search(pattern_blast_line, blast_line)
    if match:
        gene_id1 = match.group(1)
        gene_id2 = match.group(2)
        blast_identity = match.group(3)
        blast_evalue = match.group(11)
        blast_bitscore = match.group(12)
    else:
        gene_id1 = 'no match'
        gene_id2 = 'no match'
        blast_identity = 'no match'
        blast_evalue = 'no match'
        blast_bitscore = 'no match'

    return gene_id1, gene_id2, blast_identity, blast_evalue, blast_bitscore
