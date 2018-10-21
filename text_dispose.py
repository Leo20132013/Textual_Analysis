import pandas as pd
import numpy as np
import re

text_path = r'F:\AnnouncementText\IRM_QA.xlsx'
dic_path = r'C:\Users\Administrator\Desktop\Tempo\Campbell_Chinese.xlsx'
ret_path = r'C:\Users\Administrator\Desktop\Baidu_Sep_19\Que_Risk.csv'

''' 导入主表 '''
df = pd.read_excel(text_path, encoding='utf-8')
df.drop([0,1], axis='rows', inplace=True)
df.index = range(len(df))

''' 清洗文本 '''
def clean_text(rows):
	try:
		if type(rows) != np.nan:
			rows = rows.replace(" ", "")
			rows = rows.replace(",", "，")
			rows = rows.replace("\n", "")
			return rows
		else:
			return ""
	except:
		return "Error"

df['Question'] = df['Question'].apply(clean_text)
df['Answer'] = df['Answer'].apply(clean_text)

''' 导入字典 '''
dic = pd.read_excel(dic_path, header=None, encoding='utf-8')
cols = ['Type', 'Word']
dic.columns =cols

def Combine_List(rows):
    lst = [w for w in rows.split(",")]
    return lst

dic["Combine"] = (dic["Type"] + "," + dic["Word"])
dic["Combine"] = dic["Combine"].apply(Combine_List)
dic_list = list(dic.loc[dic.Type.notnull(), 'Combine'])

''' 关键词提取(关键词及其起始位置) '''
def keyword_extract(rows, wordlist):
    wordloc = []
    for word in wordlist:
        s = rows.find(word[1])
        while s != -1:
            e = s + len(word[1])
            keyword = rows[s:e]
            wordloc.append([word[0],keyword,s,e])
            s = rows.find(word[1], e)
    return wordloc

df['keyword'] = df['Question'].apply(keyword_extract, wordlist=dic_list)

''' 关键词去重 '''
def drop_subset(lst):
    dup = lst.copy()
    if len(lst) > 1:
        for i in lst:
            key_word = i
            key_i = range(i[2], i[3])
            for j in lst:
                key_j = range(j[2], j[3])
                if set(key_i) < set(key_j):
                    try:
                        dup.remove(key_word)
                    except:
                        continue
    return dup

df['keyword'] = df['keyword'].apply(drop_subset)

''' 关键词分类 '''
def risk_classfy(rows, risktype):
    riskwords = []
    for lst in rows:
        if lst[0] == risktype:
            riskwords.append(lst)
        else:
            pass
    return riskwords

df['finan'] = df['keyword'].apply(risk_classfy, risktype='Financial')
df['ido'] = df['keyword'].apply(risk_classfy, risktype='Idiosyncratic')
df['sys'] = df['keyword'].apply(risk_classfy, risktype='Systematic')
df['lg_rg'] = df['keyword'].apply(risk_classfy, risktype='LegalandRegulatory')
df['tax'] = df['keyword'].apply(risk_classfy, risktype='Tax')

''' 特定类关键词总长度 '''
def kword_len(rows):
    length = 0
    if len(rows) > 0:
        for lst in rows:
            wlen = len(lst[1])
            length += wlen
    return length

df['finan_len'] = df['finan'].apply(kword_len)
df['ido_len'] = df['ido'].apply(kword_len)
df['sys_len'] = df['sys'].apply(kword_len)
df['lg_rg_len'] = df['lg_rg'].apply(kword_len)
df['tax_len'] = df['tax'].apply(kword_len)

''' 特定类关键词在问题中出现次数 '''
def kword_count(rows):
    count = len(rows)
    return count

df['finan_count'] = df['finan'].apply(kword_count)
df['ido_count'] = df['ido'].apply(kword_count)
df['sys_count'] = df['sys'].apply(kword_count)
df['lg_rg_count'] = df['lg_rg'].apply(kword_count)
df['tax_count'] = df['tax'].apply(kword_count)

''' 问题及回答总长度(剔除数字和符号)'''
def text_len(rows):
    text = ""
    lst = re.findall(r'[\u4E00-\u9FA5A-Za-z]+',rows)
    for string in lst:
        text += string
    length = len(text)
    return length

df['Question_len'] = df['Question'].apply(text_len)
df['Answer_len'] = df['Answer'].apply(text_len)

''' 特定类关键词占总长度比例 '''
df['finan_ratio'] = df['finan_len'] / df['Question_len']
df['ido_ratio'] = df['ido_len'] / df['Question_len']
df['sys_ratio'] = df['sys_len'] / df['Question_len']
df['lg_rg_ratio'] = df['lg_rg_len'] / df['Question_len']
df['tax_ratio'] = df['tax_len'] / df['Question_len']

''' 所有类关键词占总长度比例 '''
df['total_ratio'] = (df['finan_len'] + df['ido_len'] + 
					df['sys_len'] + df['lg_rg_len'] +
					df['tax_len']) / df['Question_len']

''' 文件导出 '''
cols = ['Question','Answer','keyword','finan','ido','sys','lg_rg','tax']
df.drop(columns=cols, axis=1, inplace=True)
df.to_csv(ret_path, encoding='utf-8', index=False)