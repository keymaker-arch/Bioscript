# take a pandas series of one fpkm column in [genes,fpkm_tracking], and return the 5% minimum or 95% max value
# usage:
# df_fpkm['control'].replace(to_replace=0, value=compute_min(df_fpkm.iloc[:,2]), inplace=True)
def compute_min(sr_fpkm, rate=0.05):
    sr_tmp = sr_fpkm.dropna()
    sr_tmp = sr_tmp[~sr_fpkm.isin([0])]
    sr_tmp = sr_tmp.sort_values(ascending=True)
    line_count = sr_tmp.shape[0]

    return sr_tmp.iloc[int(line_count*rate)]


def compute_max(sr_fpkm, rate=0.95):
    sr_tmp = sr_fpkm.dropna()
    sr_tmp = sr_tmp[~sr_fpkm.isin([0])]
    sr_tmp = sr_tmp.sort_values(ascending=True)
    line_count = sr_tmp.shape[0]

    return sr_tmp.iloc[int(line_count*rate)]

