# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 21:33:44 2019

@author: johnm
"""

import os, sys, glob, warnings
import pandas as pd
import numpy as np
warnings.filterwarnings("ignore")

os.chdir(os.getcwd()+'\\historic_data\\xlsxs')
save_path = os.path.abspath(os.path.join(os.getcwd(), '..',))

class renamer():
    def __init__(self):
        self.d = dict()

    def __call__(self, x):
        if x not in self.d:
            self.d[x] = 0
            return x
        else:
            self.d[x] += 1
            return "%s %d" % (x, self.d[x])

def concatena_cols_df(df,cols,name):
    df = df.copy()
    df['dummy_col'] = 0
    for col in cols:
        df['dummy_col'] = df['dummy_col'] + df[col]
    df = df.drop(cols,axis=1)
    df[name] = df['dummy_col']
    df = df.drop(['dummy_col'],axis=1)
    return df
 
### Carrega dados dos Balanços Patrimoniais    

def corrige_df_BP(df):
    df = df.copy()
    colunas = [n.lower() for n in df.columns]

#    cols_check = [z for z in colunas if 'ativo' in z and 'aplicações' in z and not 'amortizado' in z]
#    if len(cols_check) > 0:
#        df = concatena_cols_df(df,cols_check,'ativo - aplicações financeiras')
    cols_check = [z for z in colunas if 'ativo' in z and 'imobilizado' in z]
    if len(cols_check) > 0:
        df = concatena_cols_df(df,cols_check,'ativo - imobilizado')
#    cols_check = [z for z in colunas if 'ativo' in z and 'outros' in z and not 'circulantes' in z]
#    if len(cols_check) > 0:
#        df = concatena_cols_df(df,cols_check,'ativo - outros')
#    cols_check = [z for z in colunas if 'obrigações' in z and not 'trabalhistas' in z]
#    if len(cols_check) > 0:
#        df = concatena_cols_df(df,cols_check,'passivo - obrigações')
#    cols_check = [z for z in colunas if 'passivo' in z and 'outro' in z]
#    if len(cols_check) > 0:
#        df = concatena_cols_df(df,cols_check,'passivo - outros')
    cols_check = [z for z in colunas if 'part' in z and 'acion' in z]
    if len(cols_check) > 0:
        df = concatena_cols_df(df,cols_check,'passivo - participação dos acionistas não controladores')
    cols_check = [z for z in colunas if 'pl - ' in z and 'reservas' in z]
    if len(cols_check) > 0:
        df = concatena_cols_df(df,cols_check,'pl - reservas')
    cols_check = [z for z in colunas if 'pl - ' in z and 'prejuízos acumulados' in z]
    if len(cols_check) > 0:
        df = concatena_cols_df(df,cols_check,'pl - lucros ou prejuízos acumulados')
    return df

list_of_cols = []

for fil in list(glob.glob("*.xls")):
    xls = pd.ExcelFile(fil)
    df = xls.parse('Bal. Patrim.', skiprows=1, na_values=['NA'])
    df.columns = ['safra'] + list(df.columns[1:])
    compl = ''    
    for i in range(df.shape[0]):
        if 'total' in df.loc[i,'safra'].lower():
            if 'ativo' in df.loc[i,'safra'].lower():
                compl = 'ativo - '
            elif  'passivo' in df.loc[i,'safra'].lower():
                compl = 'passivo - '
        elif 'líquido' in df.loc[i,'safra'].lower():
            compl = 'PL - '
        else:
            df.loc[i,'safra'] = compl+df.loc[i,'safra']
    df = df.set_index('safra').T
    list_of_cols = list_of_cols + list(df.columns)

list_of_cols = sorted([n.lower() for n in list(np.unique(list_of_cols))+['ticker']])

hist_data_BP = pd.DataFrame(columns=list_of_cols)
hist_data_BP = corrige_df_BP(hist_data_BP)
hist_data_BP = hist_data_BP[list(sorted(hist_data_BP.columns))]

for fil in glob.glob("*.xls"):
    xls = pd.ExcelFile(fil)
    df = xls.parse('Bal. Patrim.', skiprows=1, na_values=['NA'])
    df.columns = ['safra'] + list(df.columns[1:])
    compl = ''    
    for i in range(df.shape[0]):
        if 'total' in df.loc[i,'safra'].lower():
            if 'ativo' in df.loc[i,'safra'].lower():
                compl = 'ativo - '
                df.loc[i,'safra'] = compl+df.loc[i,'safra']
            elif  'passivo' in df.loc[i,'safra'].lower():
                compl = 'passivo - '
        elif 'líquido' in df.loc[i,'safra'].lower():
            compl = 'PL - '
        else:
            df.loc[i,'safra'] = compl+df.loc[i,'safra']
    df = df.set_index('safra').T
    df['ticker'] = fil.strip(".xls")
    df.columns = [n.lower() for n in df.columns]
    df = df.rename(columns=renamer())
#    for col in df.columns:
#        if ' 1' in col:
#            df = concatena_cols_df(df,[col[:-2],col],col[:-2])
    df = corrige_df_BP(df)
    for col in np.setdiff1d(hist_data_BP.columns,df.columns):
        df[col] = np.nan
    df = df[list(sorted(df.columns))] 
    hist_data_BP = hist_data_BP.append(df)

hist_data_BP.reset_index().rename(columns={'index':'safra'}).to_csv(save_path+'\\historico_balanco_patrimonial.csv',sep=';',encoding='latin-1',index=False)

#teste_read = pd.read_csv(save_path+'\historico_balanco_patrimonial.csv',sep=';',encoding='latin-1')

### Carrega dados dos Demonstrativos de Resultado

list_of_cols_DRE = []

for fil in list(glob.glob("*.xls")):
    xls = pd.ExcelFile(fil)
    df = xls.parse('Dem. Result.', skiprows=1, na_values=['NA'])
    df.columns = ['safra'] + list(df.columns[1:])
    df = df.set_index('safra').T
    list_of_cols_DRE = list_of_cols_DRE + list(df.columns)

list_of_cols_DRE = sorted([n.lower() for n in list(np.unique(list_of_cols_DRE))+['ticker']])
for i in range(len(list_of_cols_DRE)):
    if "/" in list_of_cols_DRE[i]:
        list_of_cols_DRE[i] = list_of_cols_DRE[i].replace("/"," ")
        
hist_data_DRE = pd.DataFrame(columns=list_of_cols_DRE)

for fil in glob.glob("*.xls"):
    xls = pd.ExcelFile(fil)
    df = xls.parse('Dem. Result.', skiprows=1, na_values=['NA'])
    df.columns = ['safra'] + list(df.columns[1:])
    for i in range(df.shape[0]):
        if '/' in df.loc[i,'safra']:
            df.loc[i,'safra'] = df.loc[i,'safra'].replace("/"," ")
    df = df.set_index('safra').T
    df['ticker'] = fil.strip(".xls")
    df.columns = [n.lower() for n in df.columns]
    for col in np.setdiff1d(hist_data_DRE.columns,df.columns):
        df[col] = np.nan
    df = df[list(sorted(df.columns))] 
    hist_data_DRE = hist_data_DRE.append(df)
    
delete_rows = [n for n in hist_data_DRE.index if "Unnamed" in n]
for r in delete_rows:
    hist_data_DRE = hist_data_DRE.drop(r)
    
hist_data_DRE.reset_index().rename(columns={'index':'safra'}).to_csv(save_path+'\\historico_DRE.csv',sep=';',encoding='latin-1',index=False)