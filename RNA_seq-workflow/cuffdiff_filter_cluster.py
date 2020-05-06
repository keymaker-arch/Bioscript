import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from ReExp import OrhoMCL


file_in = 'C:\\Users\\dell\\Desktop\\gene_exp_diff_summary.csv'
file_out_1 = 'C:\\Users\\dell\\Desktop\\gene_exp_diff_summary_filter.csv'
file_out_2 = 'C:\\Users\\dell\\Desktop\\gene_exp_diff_summary_filter_cluster.csv'

df_raw = pd.read_csv(file_in)

# filtrate data where p_value<0.05 and |FD|<=1. and replace inf to 5% rank data in columns
df_fil = df_raw[(df_raw['p_value_1h']<0.05) & (df_raw['p_value_6h']<0.05)&(df_raw['p_value']<0.05)]
df_fil = df_fil[(df_fil['log2(fold_change)_1h']>=1) | (df_fil['log2(fold_change)_1h']<=-1) & (df_fil['log2(fold_change)_6h']>=1) | (df_fil['log2(fold_change)_6h']<=-1) & (df_fil['log2(fold_change)']>=1) | (df_fil['log2(fold_change)']<=-1)]
df_fil = df_fil.set_index('gene_id' ,drop=True)
df_fil.columns = ['FD_1h', 'p_value_1h', 'FD_6h','p_value_6h', 'FD_3h','p_value_3h']

tmp = df_fil.loc[:, ['FD_1h']]
tmp = tmp[~tmp['FD_1h'].isin([np.inf])]
tmp = tmp[~tmp['FD_1h'].isin([-np.inf])]
tmp = tmp.sort_values(by='FD_1h')
min_1h = tmp.iloc[int(tmp.shape[0]*0.05), 0]
max_1h = tmp.iloc[int(tmp.shape[0]*0.95), 0]

tmp = df_fil.loc[:, ['FD_3h']]
tmp = tmp[~tmp['FD_3h'].isin([np.inf])]
tmp = tmp[~tmp['FD_3h'].isin([-np.inf])]
tmp = tmp.sort_values(by='FD_3h')
min_3h = tmp.iloc[int(tmp.shape[0]*0.05), 0]
max_3h = tmp.iloc[int(tmp.shape[0]*0.95), 0]

tmp = df_fil.loc[:, ['FD_6h']]
tmp = tmp[~tmp['FD_6h'].isin([np.inf])]
tmp = tmp[~tmp['FD_6h'].isin([-np.inf])]
tmp = tmp.sort_values(by='FD_6h')
min_6h = tmp.iloc[int(tmp.shape[0]*0.05), 0]
max_6h = tmp.iloc[int(tmp.shape[0]*0.95), 0]

df_fil.loc[df_fil['FD_1h']==np.inf, 'FD_1h'] = max_1h
df_fil.loc[df_fil['FD_3h']==np.inf, 'FD_3h'] = max_3h
df_fil.loc[df_fil['FD_6h']==np.inf, 'FD_6h'] = max_6h
df_fil.loc[df_fil['FD_1h']==-np.inf, 'FD_1h'] = min_1h
df_fil.loc[df_fil['FD_3h']==-np.inf, 'FD_3h'] = min_3h
df_fil.loc[df_fil['FD_6h']==-np.inf, 'FD_6h'] = min_6h

print(df_fil.head(200))
# df_fil.to_csv(file_out_1)

# hierarchical cluster
# df_fd = df_fil.loc[:, ['FD_1h', 'FD_6h', 'FD_3h']]
# # print(df_fd.head(100))
# # row_cluster = linkage(pdist(df_fd,metric='euclidean'), method='complete')
# # row_dendr = dendrogram(row_cluster, labels=df_fd.index)
# # plt.tight_layout()
# # plt.xticks([])
# # plt.show()