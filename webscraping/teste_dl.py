# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 20:44:14 2019

@author: johnm
"""

import urllib.request
import webbrowser
import pandas as pd
import pickle
import os, sys, glob

current_path = os.getcwd()
ws_path = '\\Documents\\python\\company_research\\webscraping\\'
url_dl="https://www.fundamentus.com.br/planilhas.php?SID=500p0ehvq8krd7tvl75pa8jnk2"

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
raw_stocks_list = pickle.load(open(current_path + ws_path + 'current_tickers.pkl',mode='rb'))

for tick in raw_stocks_list:
    webbrowser.get(chrome_path).open_new("https://www.fundamentus.com.br/balancos.php?papel=%s&tipo=1"%tick)
    urllib.request.urlretrieve(url_dl, current_path + ws_path + 'historic_data\\%s.zip'%tick)
    
# Now lets unzip stuff!

import zipfile
os.chdir(current_path+ws_path+'historic_data')

for fil in glob.glob("*.zip"):
    try:
        with zipfile.ZipFile(fil, 'r') as zip_ref:
            zip_ref.extractall('xlsxs')
        os.rename('xlsxs\\balanco.xls','xlsxs\\%s'%fil.strip('.zip')+'.xls')
    except:
        print("Removing %s for being corrupted"%fil)
        os.remove(fil)
