Python 3.10.7 (tags/v3.10.7:6cc6b13, Sep  5 2022, 14:08:36) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import sys
import pandas as pd
... PATH=sys.argv[1]
... scopus=pd.read_csv(PATH,sep=',')
... scopus.dropna(axis=0, how='any',subset=['Correspondence Address','Authors'],inplace=True)
... scopus[['cor_name','cor_aff','email']]=scopus['Correspondence Address'].str.split(';',expand=True).iloc[:,:3]
... scopus['cor_ins']=scopus['cor_aff'].fillna('Nothing').map(lambda x: x.split(',')[0])
... scopus['country']=scopus['cor_aff'].fillna('Nothing').map(lambda x: x.split(',')[-1])
... scopus['email']=scopus['email'].astype(str)
... scopus['email']=scopus['email'].map(lambda x: x[7:] if x is not None else 0)
... ids=[]
... names=[]
... for i in range (len(scopus)):
...     try:
...         name=scopus['cor_name'].iloc[i].replace(',','')
...         name_list=[]
...         for lname, fname in  [q.split() for q in scopus['Authors'].iloc[i].split(';')]:
...           name_list.append(fname+' '+lname)
...         ind=name_list.index(name)
...         ids.append(list(scopus['Author(s) ID'].iloc[i].split(';'))[ind].strip())
...         full_name=list(scopus['Author full names'].iloc[i].split(';'))[ind]
...         name_end=list(scopus['Author full names'].iloc[i].split(';'))[ind].find('(')
...         names.append(full_name[:name_end])
...     except ValueError:
...         ids.append(0)
...         names.append(0)
... weblist = ['https://www.scopus.com/authid/detail.uri?authorId='+str(x) for x in ids]
... scopus=scopus.reset_index().drop('index',axis=1)
... scopus['cor_id']=pd.Series(ids)
... scopus['cor_fullname']=pd.Series(names)
... scopus['URL']=pd.Series(weblist)
... new_scopus=scopus[['cor_name','cor_fullname','cor_id','cor_aff','email','cor_ins','country','Author Keywords','Indexed Keywords','URL']]
... new_scopus.drop(new_scopus[new_scopus['cor_id']==0].index,axis=0,inplace=True)
