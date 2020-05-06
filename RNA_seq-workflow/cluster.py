import pandas as pd
import seaborn as sns


file_diff = 'C:\\Users\\dell\\Desktop\\sulab\\cuffdiff\\gene_exp_diff_summary_filter.csv'
df_diff = pd.read_csv(file_diff)
df_diff.set_index('gene_id', drop=True, inplace=True)
df_diff = df_diff.loc[:, ['FD_1h', 'FD_3h', 'FD_6h']]

# cluster = sch.linkage(df_diff)
#
# print(cluster)
# sns.clustermap(df_diff, method='average', metric='euclidean', col_cluster=False, cmap='RdBu_r', center=0.0, vmin=-3, vmax=3, row_colors=df_diff)
clustered = sns.clustermap(df_diff, method='average', metric='euclidean', col_cluster=False, cmap='RdBu_r', center=0.0, vmin=-3, vmax=3)
clustered.savefig()
reodered_index = clustered.dendrogram_row.reordered_ind

df_diff_clustered = pd.DataFrame()
for index in reodered_index:
    df_diff_clustered = df_diff_clustered.append(df_diff.iloc[index, :])

df_diff_clustered.to_csv('C:\\Users\\dell\\Desktop\\clustered_gene_exp_diff.csv')
