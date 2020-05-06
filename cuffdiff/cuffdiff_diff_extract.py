import pandas as pd


file_in = 'C:\\Users\\dell\\Desktop\\gene_exp_diff.csv'
file_out = 'C:\\Users\\dell\\Desktop\\gene_exp_diff_summary.csv'

df_raw = pd.read_csv(file_in)

df_info = df_raw.loc[:,['gene_id', 'sample_1','sample_2', 'log2(fold_change)', 'p_value']]
df_0h = df_info.loc[df_info['sample_1']=='0h']

df_0h_1h = df_0h.loc[df_0h['sample_2'] == '1h']
df_0h_3h = df_0h.loc[df_0h['sample_2'] == '3h']
df_0h_6h = df_0h.loc[df_0h['sample_2'] == '6h']
df_0h_1h.set_index('gene_id', drop=True, inplace=True)
df_0h_3h.set_index('gene_id', drop=True, inplace=True)
df_0h_6h.set_index('gene_id', drop=True, inplace=True)

df_rtn = df_0h_1h.loc[:,['log2(fold_change)', 'p_value']]
df_rtn.columns=['log2(fold_change)_1h', 'p_value_1h']
df_rtn = df_rtn.join(df_0h_3h.loc[:,['log2(fold_change)', 'p_value']], how='right',lsuffix='_3h')
df_rtn = df_rtn.join(df_0h_6h.loc[:,['log2(fold_change)', 'p_value']], how='right',lsuffix='_6h')
df_rtn = df_rtn.replace('#NAME?', '-inf')

df_rtn.to_csv(file_out)