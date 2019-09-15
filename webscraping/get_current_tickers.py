# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 11:05:37 2019

@author: johnmattox
"""

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import os, sys
import pickle

current_path = os.getcwd()
main_path = ""
for el in current_path.split('\\')[:-1]:
    main_path=main_path+el+"\\"
sys.path.insert(1,main_path)
 
import utilities as ut
import datetime
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
current_date = datetime.datetime.now()
verbose=True

if verbose:
    print('Webscraping for raw information: Balance Sheets and Profit&Loss Statements')

base_url = 'https://www.fundamentus.com.br/'
raw_info_url = 'https://www.fundamentus.com.br/detalhes.php'

if verbose:
    print('Connecting to website')
    
req = Request(url=raw_info_url,headers=headers)
uClient = urlopen(req)
page_html = uClient.read()
uClient.close()

raw_soup = soup(page_html, "html.parser")
names_table = raw_soup.find("table",{"id":"test1"}).tbody.findAll("tr")

current_trimester = ut.yearmonth_to_trimester(current_date.month)
min_acceptable_data_time = ut.back_n_trimesters(current_date.year,current_trimester,1)
raw_stocks_list = {}

for i,row in enumerate(names_table,0):
    ticker = row.findAll("td")[0].text.strip()
    url_ticker = base_url+row.findAll("td")[0].a['href'].strip()
    
    req = Request(url=url_ticker,headers=headers)
    uClient = urlopen(req)
    page_html = uClient.read()
    uClient.close()
    ticker_soup = soup(page_html, "html.parser")
    
    if ticker_soup.find("div",{"class":"conteudo clearfix"}).h1 is None:
        year_ticker_data = int(ticker_soup.findAll('table',{'class':'w728'})[1].findAll('td',{'class':'data w2'})[0].text.strip()[-4:])
        month_ticker_data = int(ticker_soup.findAll('table',{'class':'w728'})[1].findAll('td',{'class':'data w2'})[0].text.strip()[-7:-5])
        if (((100*year_ticker_data)+month_ticker_data) >= min_acceptable_data_time):
            raw_stocks_list[ticker] = {}
            raw_stocks_list[ticker]['name'] = row.findAll("td")[1].text.strip()
            raw_stocks_list[ticker]['corp name'] = row.findAll("td")[2].text.strip()
            raw_stocks_list[ticker]['url'] = url_ticker
    
    if verbose:
        print("\rCollecting data - Conclusion: %.2f%%"%((i+1)*100.0/len(names_table)),end='')

pickle.dump(list(raw_stocks_list),open('current_tickers.pkl',mode='wb'))