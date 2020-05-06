# collect re exp using in all kinds of bioinfo files
# each software corresponds to one class


# OrthoMCL
# used to detect homologous gene cluster in organisms
class OrhoMCL():
    # using this exp to match all gene id in one cluster
    # when using this exp, use re.findall() to get a list of genes in one cluster(one csv cell)
    pattern_gene = r'\|([A-Z,a-z,\_,\d,\.]+);'


class MCScanX():
    # the following exps are used to generate MCScanX gff file from standard gff file

    # use this exp to check if the line is a CDs
    pattern_cds = '\tCDS\t'

    # extract gene loc in the first string in the line
    pattern_loc = '^(.*?)\t'

    # extract gene name in the note column if the gene id in name parameter
    # check if the gene id is after this parameter when using
    pattern_id = ';Name=(.*?);'
    # pattern_id = ';ID=(.*?);'

    # extract start and end of the gene
    pattern_begin_end = '\t(\d+)\t(\d+)\t'


class Blast():
    # use this exo to match a full line of a m8 blast file
    pattern_blast_line = '^(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$'
    # gene_id1 = match.group(1)
    # gene_id2 = match.group(2)
    # blast_identity = match.group(3)
    # blast_evalue = match.group(11)
    # blast_bitscore = match.group(12)