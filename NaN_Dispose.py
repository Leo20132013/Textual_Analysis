# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 17:48:54 2018

@author: Administrator
"""
'''
定义数据清洗函数，将文本中的换行符及英文逗号替换，并将其他非GBK编码文本强行转换
'''
def to_csv(df, path):
    with open(path, 'w', encoding='GBK', errors='ignore') as f:
        fline=','.join(list(df.columns))+"\n"
        f.write(fline)
        x, y = df.shape
        for i in range(x):
            line=""
            for j in range(y):
                line = line+str(df.iloc[i,j]).replace("\n","").replace(",","，")+','
            line=line[:-1]+"\n"
            f.write(line)

#*---------------------------------------------------------------------------*#
from tqdm import tqdm
import pandas as pd
from aip import AipNlp

path_main = r'F:\AnnouncementText\IRM_QA.xlsx'
path_app = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Question_Senti.csv'

df = pd.read_excel(path_main, encoding='utf-8')
df.drop([0,1], axis='rows', inplace=True)
df.index = range(len(df))

app = pd.read_csv(path_app, encoding='utf-8')

missing = df.loc[app['confi_que'].isnull(), :]
missing['Question'].isnull().sum()
''' 不是因问题缺省而导致的缺漏值 '''
missing.drop('Answer', axis=1, inplace=True)

to_csv(missing, r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Question_Miss.csv')

que_retry = pd.read_csv(r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Question_Miss.csv',
               encoding='GBK')

APP_ID = '11788538'
API_KEY = 'BcIhkEUdtaKmaqGtEIAXG3r2'
SECRET_KEY = '6Rsdrv6C2FTqEVbEeXroIEWtGjOk3BSI'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

''' 新建4个空值列 '''
que_retry['confi_que'] = 'NaN'
que_retry['neg_prob_que'] = 'NaN'
que_retry['pos_prob_que'] = 'NaN'
que_retry['senti_que'] = 'NaN'

for i in tqdm(range(len(que_retry))):
    text_que = que_retry['Question'][i]
    ''' 调用情感倾向分析 '''
    ''' Question '''
    try:
        tempo_que = client.sentimentClassify(text_que)
    except:
        tempo_que = {}
    else:
        try:
            que_retry.at[i,'confi_que'] = tempo_que['items'][0]['confidence']
            que_retry.at[i,'neg_prob_que'] = tempo_que['items'][0]['negative_prob']
            que_retry.at[i,'pos_prob_que'] = tempo_que['items'][0]['positive_prob']
            que_retry.at[i,'senti_que'] = tempo_que['items'][0]['sentiment']
        except KeyError:
            pass

que_retry.drop('Question', axis=1, inplace=True)
que_retry.to_csv(r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Que_Miss_Retry.csv',
           encoding='utf-8', index=False)

#*---------------------------------------------------------------------------*#
from tqdm import tqdm
import pandas as pd
from aip import AipNlp

path_main = r'F:\AnnouncementText\IRM_QA.xlsx'
path_app = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Answer_Senti.csv'

df = pd.read_excel(path_main, encoding='utf-8')
df.drop([0,1], axis='rows', inplace=True)
df.index = range(len(df))

app = pd.read_csv(path_app, encoding='utf-8')

missing = df.loc[app['confi_ans'].isnull(), :]
missing['Question'].isnull().sum()
''' 不是因问题缺省而导致的缺漏值 '''
missing.drop('Question', axis=1, inplace=True)
missing.index = range(len(missing))

to_csv(missing, r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Answer_Miss.csv')

ans_retry = pd.read_csv(r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Answer_Miss.csv',
               encoding='GBK')

APP_ID = '10771642'
API_KEY = '7QKEGf47U1trhYptTB3bM4gP'
SECRET_KEY = 'sdDSGirKljr4ijyRGYFOgP4VEtoP7W6a'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

''' 新建4个空值列 '''
ans_retry['confi_ans'] = 'NaN'
ans_retry['neg_prob_ans'] = 'NaN'
ans_retry['pos_prob_ans'] = 'NaN'
ans_retry['senti_ans'] = 'NaN'

for i in tqdm(range(len(ans_retry))):
    text_ans = ans_retry['Answer'][i]
    ''' 调用情感倾向分析 '''
    ''' Answer '''
    try:
        tempo_ans = client.sentimentClassify(text_ans[0:1024])
    except:
        tempo_ans = {}
    else:
        try:
            ans_retry.at[i,'confi_ans'] = tempo_ans['items'][0]['confidence']
            ans_retry.at[i,'neg_prob_ans'] = tempo_ans['items'][0]['negative_prob']
            ans_retry.at[i,'pos_prob_ans'] = tempo_ans['items'][0]['positive_prob']
            ans_retry.at[i,'senti_ans'] = tempo_ans['items'][0]['sentiment']
        except KeyError:
            pass

ans_retry.drop('Answer', axis=1, inplace=True)
ans_retry.to_csv(r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Ans_Miss_Retry.csv',
           encoding='utf-8', index=False)

#*---------------------------------------------------------------------------*#
from tqdm import tqdm
import pandas as pd
from aip import AipNlp

path_main = r'F:\AnnouncementText\IRM_QA.xlsx'
path_app = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\wordlist_new.csv'

df = pd.read_excel(path_main, encoding='utf-8')
df.drop([0,1], axis='rows', inplace=True)
df.index = range(len(df))

app = pd.read_csv(path_app, encoding='GBK')

missing = df.loc[app['WordList'].isnull(), :]
missing['Question'].isnull().sum()

missing.drop('Answer', axis=1, inplace=True)

to_csv(missing, r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Cut_Miss.csv')

cut_retry = pd.read_csv(r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Cut_Miss.csv',
               encoding='GBK')

APP_ID = '14201923'
API_KEY = 'IqxP6YZ0LbHRUcBPs3gXvkUX'
SECRET_KEY = 'uCllQY08wOGwwCvZvVkGnMiDq857GC5Q'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

cut_retry['WordList'] = 'NaN'

for i in tqdm(range(len(cut_retry))):
    text = cut_retry['Question'][i]
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
                cut_retry.at[i, 'WordList'] = rettext
        except:
            pass

cut_retry.drop('Question', axis=1, inplace=True)
cut_retry.to_csv(r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Cut_Miss_Retry.csv',
           encoding='utf-8', index=False)

#*---------------------------------------------------------------------------*#
''' Question '''
path1 = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Question_Senti.csv'
path2 = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Que_Miss_Retry.csv'
outpath1 = r'C:\Users\Administrator\Desktop\Baidu_Sep_19\Que_Final.csv'

df = pd.read_csv(path1, encoding='utf-8')
fail_que = df.loc[df.confi_que.isnull(), :]
suc_que = df.loc[~df.index.isin(fail_que.index), :]

retry_que = pd.read_csv(path2, encoding='utf-8')

Que_Complete = pd.concat([suc_que, retry_que], axis=0)
Que_Complete.sort_values(by=['Symbol', 'ReportDate', 'Rank'], inplace=True)
Que_Complete.index = range(len(Que_Complete))
Que_Complete.to_csv(outpath1, encoding='utf-8', index=False)

''' Answer '''
path3 = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Answer_Senti.csv'
path4 = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Ans_Miss_Retry.csv'
outpath2 = r'C:\Users\Administrator\Desktop\Baidu_Sep_19\Ans_Final.csv'

df = pd.read_csv(path3, encoding='utf-8')
fail_ans = df.loc[df.confi_ans.isnull(), :]
suc_ans = df.loc[~df.index.isin(fail_ans.index), :]

retry_ans = pd.read_csv(path4, encoding='utf-8')

Ans_Complete = pd.concat([suc_ans, retry_ans], axis=0)
Ans_Complete.sort_values(by=['Symbol', 'ReportDate', 'Rank'], inplace=True)
Ans_Complete.index = range(len(Ans_Complete))
Ans_Complete.to_csv(outpath2, encoding='utf-8', index=False)

''' WordList '''
'''
有问题
'''
path5 = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\wordlist_new.csv'
path6 = r'C:\Users\Administrator\Desktop\Baidu_Sep_17\Cut_Miss_Retry.csv'
outpath3 = r'C:\Users\Administrator\Desktop\Baidu_Sep_19\Cut_Final.csv'

df = pd.read_csv(path5, encoding='GBK')
fail_cut = df.loc[df['WordList'].isnull(), :]
suc_cut = df.loc[~df.index.isin(fail_cut.index), :]

retry_cut = pd.read_csv(path6, encoding='utf-8')

Cut_Complete = pd.concat([suc_cut, retry_cut], axis=0)
Cut_Complete.sort_values(by=['Symbol', 'ReportDate', 'Rank'], inplace=True)

Cut_Complete['Symbol'] = Cut_Complete['Symbol'].astype('object')
Cut_Complete['Rank'] = Cut_Complete['Rank'].astype('object')

Cut_Complete.index = range(len(Cut_Complete))
Cut_Complete.to_csv(outpath3, encoding='utf-8', index=False)

#*---------------------------------------------------------------------------*#
''' 词频统计 '''
df = pd.read_csv(r'C:\Users\Administrator\Desktop\Baidu_Sep_19\Cut_Final.csv',
           encoding='utf-8')

df['wd'] = 'NaN'
for i in tqdm(range(len(df))):
    wd = df['WordList'][i].split('/')
    df.at[i, 'wd'] = wd

freq = []
for i in tqdm(range(len(df))):
    wordlist = df['wd'][i]
    for word in wordlist:
        if word not in freq:
            freq.append(word)
        else:
            pass

freq_dic = {}.fromkeys(freq, 0)
for i in tqdm(range(len(df))):
    wl = df['wd'][i]
    for word in wl:
        if word in freq:
            freq_dic[word] += 1
        else:
            continue
ret_path = r'C:\Users\Administrator\Desktop\Baidu_Sep_19\freq.csv'
with open(ret_path, 'w', encoding='utf-8') as f:
    for key in freq_dic.keys():
        f.write("{},{}\n".format(key, freq_dic[key]))















