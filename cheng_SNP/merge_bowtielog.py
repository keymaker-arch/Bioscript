import pandas as pd


file_path = 'C:\\Users\\dell\\Desktop\\PH207_SRR _tmp.xlsx'
fp = open(file_path, 'r')
df_acc = pd.read_excel(file_path, sheet_name='SRR汇总')
df_log = pd.read_excel(file_path, sheet_name='bowtielog')

df_acc = df_acc.merge(df_log, how='outer')
print(df_acc)
writer = pd.ExcelWriter(file_path)
df_acc.to_excel(writer, 'sheet_test')
writer.save()