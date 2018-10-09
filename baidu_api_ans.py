# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 10:28:18 2018

@author: Leo
"""
import pandas as pd
from aip import AipNlp
import time

APP_ID = '10771642'
API_KEY = '7QKEGf47U1trhYptTB3bM4gP'
SECRET_KEY = 'sdDSGirKljr4ijyRGYFOgP4VEtoP7W6a'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

df = pd.read_excel(r'F:\AnnouncementText\IRM_QA.xlsx', encoding='utf-8')
df.drop([0,1], axis='rows', inplace=True)
df.index = range(len(df))

df = df[:100]

''' 新建4个空值列 '''
df['confi_ans'] = 'NaN'
df['neg_prob_ans'] = 'NaN'
df['pos_prob_ans'] = 'NaN'
df['senti_ans'] = 'NaN'

start_time = time.time()
for i in range(len(df)):
       text_ans = df['Answer'][i]
       ''' 调用情感倾向分析 '''
       ''' Answer '''
       try:
              tempo_ans = client.sentimentClassify(text_ans[0:1024])
       except:
              tempo_ans = {}
       else:
              try:
                     df.at[i,'confi_ans'] = tempo_ans['items'][0]['confidence']
                     df.at[i,'neg_prob_ans'] = tempo_ans['items'][0]['negative_prob']
                     df.at[i,'pos_prob_ans'] = tempo_ans['items'][0]['positive_prob']
                     df.at[i,'senti_ans'] = tempo_ans['items'][0]['sentiment']
              except KeyError:
                     pass
       time.sleep(0.1)
       end_time = time.time()
       remain_time = (end_time - start_time) / (i + 1) * (len(df) - (i + 1))
       print("\r{:>6.2f}% Done, Time Remained: {:04}:{:02}:{:02}".format(
                     (i + 1) * 100 / len(df), int(remain_time // 3600), 
                     int(remain_time // 60 % 60), int(remain_time % 60)),
              end="")
  
df.drop(['Question', 'Answer'], axis=1, inplace=True)
ret_path = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Answer_Senti.csv' 
df.to_csv(ret_path, encoding='utf-8', index=False)