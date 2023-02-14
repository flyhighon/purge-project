#purge tool step one 
#from raw scopus csv file e.g scopus.csv to processed csvfile e.g. output
#usage: python3 purge1.py [scopus filepath] (preferably full path)
import sys
import pandas as pd
ids=[]
path = sys.argv[1]
scopus=pd.read_csv('/Users/tanfei/Documents/SpringerNature/purge/scopus.csv',sep=',') #import
scopus.dropna(axis=0, how='any',subset=['Correspondence Address'],inplace=True) # delete rows with no corresponding author  data
scopus[['cor_name','cor_aff','email']]=scopus['Correspondence Address'].str.split(';',expand=True).iloc[:,:3] # separate columns
scopus['cor_ins']=scopus['cor_aff'].dropna().map(lambda x: x.split(',')[0]) # expand column
scopus['country']=scopus['cor_aff'].dropna().map(lambda x: x.split(',')[-1])
scopus['email']=scopus['email'].map(lambda x: x[7:] if x is not None else 0) #processing
for i in range (len(scopus)):  #finding author id
    try:
        name=scopus['cor_name'].iloc[i].replace(',','')
        list(map(str.strip, list(scopus['Authors'].iloc[i].split(',')))).index(name)
        ind=[x.strip() for x in list(scopus['Authors'].iloc[i].split(','))].index(name)
        ids.append(list(scopus['Author(s) ID'].iloc[i].split(';'))[ind])
    except ValueError:
        ids.append(0)
weblist = ['https://www.scopus.com/authid/detail.uri?authorId='+str(x) for x in ids]
scopus=scopus.reset_index().drop('index',axis=1)
scopus['cor_id']=pd.Series(ids) #author id and url integration
scopus['URL']=pd.Series(weblist)
new_scopus=scopus[['cor_name','cor_id','cor_aff','email','cor_ins','country','Author Keywords','Index Keywords','URL']]
new_scopus.drop(new_scopus[new_scopus['cor_id']==0].index,axis=0,inplace=True)
new_scopus.to_csv('output.csv',encoding='utf_8_sig')