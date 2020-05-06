import re


# take in a pandas dataframe of ortho genes and return a triple nesting list
def get_ortho_gene(species_name_list, this_df_ortho, pattern_gene = r'\|([A-Z,a-z,\_,\d,\.]+);'):
    df_ortho = this_df_ortho.loc[:, species_name_list]
    df_ortho = df_ortho.dropna()
    ortho_list = []
    for i in range(0, df_ortho.shape[0]):
        tmp_list = []
        for j in range(0, len(species_name_list)):
            info = df_ortho.iloc[i, j]
            gene = re.findall(pattern_gene, info)
            tmp_list.append(gene)

        ortho_list.append(tmp_list)

    return ortho_list


# take in list from get_ortho_gene and write to a txt file
# each species a line, seperate clusters with '##' and replace vacancy with 'null'
def write_ortho_genes(ortho_list, f_out):
    for gene_cluster in ortho_list:
        lenghth = 0
        for gene_list in gene_cluster:
            if len(gene_list) > lenghth:
                lenghth = len(gene_list)

        for gene_list in gene_cluster:
            for i in range(0, lenghth-len(gene_list)):
                gene_list.append('null')

        for gene_list in gene_cluster:
            for gene in gene_list:
                f_out.write(gene+'\t')
            f_out.write('\n')

        f_out.write('##\n')
    f_out.close()