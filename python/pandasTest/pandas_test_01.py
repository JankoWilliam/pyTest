# coding=gbk

import pandas as pd

read_excel = 'C:\\Users\\ChuangLan\\Desktop\\company_total_score_l.xlsx'
data = pd.read_excel(read_excel,index_col='total_score')
print(data.describe())