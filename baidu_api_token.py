# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 13:33:48 2018

@author: Leo
"""

import pandas as pd
from aip import AipNlp
import time

#*---------------------------------------------------------------------------*#
path = r'F:\AnnouncementText\IRM_QA.xlsx'
ret_path = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\WordList.csv'

df = pd.read_excel(path, encoding='GBK')
df.drop([0,1], axis='rows', inplace=True)
df.index = range(len(df))

APP_ID = '14201923'
API_KEY = 'IqxP6YZ0LbHRUcBPs3gXvkUX'
SECRET_KEY = 'uCllQY08wOGwwCvZvVkGnMiDq857GC5Q' 
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

df['WordList'] = 'NaN'
df = df[:100]

start_time = time.time()
for i in range(len(df)):
       text = df['Question'][i]
       ''' 调用词法分析 '''
       try:
              returns = client.lexerCustom(text)
       except:
              returns = {}
       else:
              try:
                     if len(returns['items']) == 0:
                            pass
                     else:
                            wordlist = []
                            for j in range(len(returns['items'])):
                                   word = returns['items'][j]['item']
                                   wordlist.append(word)
                            rettext = "/".join(wordlist)
                            df.at[i, 'WordList'] = rettext
              except:
                     pass
       time.sleep(0.05)
       end_time = time.time()
       remain_time = (end_time - start_time) / (i + 1) * (len(df) - (i + 1))
       print("\r{:>6.2f}% Done, Time Remained: {:04}:{:02}:{:02}".format(
                     (i + 1) * 100 / len(df), int(remain_time // 3600), 
                     int(remain_time // 60 % 60), int(remain_time % 60)),
              end="")                                 

df.drop(['Question', 'Answer'], axis=1, inplace=True)
df.to_csv(ret_path, encoding='utf-8', index=False)
#*---------------------------------------------------------------------------*#




