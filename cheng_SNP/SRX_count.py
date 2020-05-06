import pandas as pd


target_csv = 'C:\\Users\\dell\\Desktop\\chenglab\\records\\PH207_sra_result.csv'
result = 'C:\\Users\\dell\\Desktop\\chenglab\\records\\PH207_srp_count.csv'
# result = 'C:\\Users\\dell\\Desktop\\chenglab\\records\\B73_srp_count.xlsx'


print('reading csv...')
df = pd.read_csv(target_csv)

srp = df.loc[:, ['Experiment Accession', 'Study Accession']]


srp_count = srp.groupby('Study Accession').count()
srp_count.columns = ['SRX Count']

srp_all = srp.shape[0]

rate = []
for i in range(0,srp_count.shape[0]):
    tmp = int(srp_count.iloc[i, 0])/srp_all
    rate.append('%.2f%%' % (tmp*100))

srp_count['SRX Count Rate'] = rate
srp_count = srp_count.sort_values(by='SRX Count', ascending=False)

srp_count.loc['total'] = [srp_all, '100%']
# print(srp_count)

run = df.loc[: ,['Study Accession', 'Total RUNs']]
run = run.groupby('Study Accession').sum()
run.loc['total'] = run.sum()

srp_count = srp_count.join(run)
print(srp_count)

srp_count.to_csv(result)
# srp_count.to_excel(result)