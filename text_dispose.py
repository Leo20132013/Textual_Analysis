import pandas as pd
import numpy as np

text_path = r'F:\AnnouncementText\IRM_QA.xlsx'
dic_path = r'C:\Users\Administrator\Desktop\Tempo\Campbell_Chinese.xlsx'

df = pd.read_excel(text_path, encoding='utf-8')
df.drop([0,1], axis='rows', inplace=True)
df.index = range(len(df))

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

dic = pd.read_excel(dic_path, header=None, encoding='utf-8')
cols = ['Type', 'Word']
dic.columns =cols

def Combine_List(rows):
    lst = [w for w in rows.split(",")]
    return lst

dic["Combine"] = (dic["Type"] + "," + dic["Word"])
dic["Combine"] = dic["Combine"].apply(Combine_List)
dic_list = list(dic.loc[dic.Type.notnull(), 'Combine'])

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

def drop_subset(lst):
    dup = lst
    if len(lst) > 1:
        for i in lst:
            key_word = i
            key_i = range(i[2], i[3])
            for j in lst:
                key_j = range(j[2], j[3])
                if set(key_i) < set(key_j):
                    dup.remove(key_word)
                else:
                    pass
    return dup

df['keyword'] = df['keyword'].apply(drop_subset)