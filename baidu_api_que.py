# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 10:28:18 2018

@author: Leo
"""
import pandas as pd
from aip import AipNlp
import time

APP_ID = '11788538'
API_KEY = 'BcIhkEUdtaKmaqGtEIAXG3r2'
SECRET_KEY = '6Rsdrv6C2FTqEVbEeXroIEWtGjOk3BSI'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

df = pd.read_excel(r'F:\AnnouncementText\IRM_QA.xlsx', encoding='utf-8')
df.drop([0,1], axis='rows', inplace=True)
df.index = range(len(df))

df = df[:100]

''' 新建4个空值列 '''
df['confi_que'] = 'NaN'
df['neg_prob_que'] = 'NaN'
df['pos_prob_que'] = 'NaN'
df['senti_que'] = 'NaN'

start_time = time.time()
for i in range(len(df)):
    text_que = df['Question'][i]
    ''' 调用情感倾向分析 '''
    ''' Question '''
    try:
        tempo_que = client.sentimentClassify(text_que)
    except:
        tempo_que = {}
    else:
        try:
            df.at[i,'confi_que'] = tempo_que['items'][0]['confidence']
            df.at[i,'neg_prob_que'] = tempo_que['items'][0]['negative_prob']
            df.at[i,'pos_prob_que'] = tempo_que['items'][0]['positive_prob']
            df.at[i,'senti_que'] = tempo_que['items'][0]['sentiment']
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
ret_path = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Question_Senti.csv'
df.to_csv(ret_path, encoding='utf-8', index=False)