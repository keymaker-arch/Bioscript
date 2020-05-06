import pandas as pd


def get_clustered_table(df_unclustered, sns_cluster, reorder_row=True, reorder_col=False):
    tmp_df = pd.DataFrame()
    reordered_row_index = sns_cluster.clustered.dendrogram_row.reordered_ind
    reordered_col_index = sns_cluster.clustered.dendrogram_col.reordered_ind

    if reorder_row and not reorder_col:
        for index in reordered_row_index:
            tmp_df = tmp_df.append(df_unclustered.iloc[index, :])

    if reorder_col and not reorder_row:
        col_list = list(df_unclustered.columns.values)
        for index in reordered_col_index:
            tmp_df[col_list[index]] = df_unclustered.iloc[:, index]

    if reorder_row and reorder_col:
        col_list = list(df_unclustered.columns.values)
        for index in reordered_col_index:
            tmp_df[col_list[index]] = df_unclustered.iloc[:, index]
        for index in reordered_row_index:
            tmp_df = tmp_df.append(df_unclustered.iloc[index, :])

    return tmp_df