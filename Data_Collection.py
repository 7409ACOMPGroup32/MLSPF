import pandas as pd
import numpy as np
import datetime
import seaborn as sns
sns.set_style('whitegrid')
from os import listdir
from os.path import isfile, join
from pandas_datareader import data
import yfinance as yf
from pandas_datareader import wb

import quandl
import pandas_datareader as pdr
import numpy as np

from datetime import date

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import copy
from tqdm import tqdm

import math
# import pmdarima as pm
yf.pdr_override()

start_date = "2015-01-01"
end_date = "2022-12-31"

stock_name = 'MSFT'
stock_df = data.get_data_yahoo(tickers=stock_name, start = start_date, end = end_date)
stock_df.reset_index(inplace=True)
stock_df

general_information = ['^DJI', '^IXIC', '^GSPC', '^RLG', '^NYA', 'DX-Y.NYB', 'EURUSD=X', 'GBPUSD=X', 'GC=F', 'SI=F', 'CL=F']
general_df = []

for index, the_name in enumerate(general_information):
    stock_df = data.get_data_yahoo(tickers=the_name, start=start_date, end=end_date)
    stock_df.reset_index(inplace=True)
    print(the_name)
    print(stock_df.head())
    if index == 0:
        general_df = stock_df[["Date", "Close"]]
        general_df = general_df.rename(columns={"Close": str(the_name)+"_Close"})
    else:
        general_df = pd.merge(general_df, stock_df[["Date", "Close"]].rename(columns={"Close": str(the_name)+"_Close"}), on="Date")


# state_var = {'inflation':'FP.CPI.TOTL.ZG', 'GDP':'NY.GDP.PCAP.KD', 'GDPpercapita':'NY.GDP.PCAP.CD', 'Grossfixedcapital':'NE.GDI.FTOT.CD','CO2':'SP.POP.TOTL', \
#              'Stockstradedpergdp':'CM.MKT.TRAD.GD.ZS'}
# selected_countries=['US', 'CA', 'MX']
# print(general_df.head())
# for the_key in state_var:
#     print(state_var[the_key])
#     the_df = wb.download(indicator=state_var[the_key], country=selected_countries, start=start_date, end=end_date)
#     print(the_df.head())
#     # general_df = pd.merge(general_df, stock_df[["Date", "Close"]].rename(columns={"Close": str(the_name) + "_Close"}),
#     #                       on="Date")

report_list = [
  'WM1NS', # M1 Supply
  'WM2NS', # M2 Supply
  'ICSA', # Unemployment
  'CCSA', # Continued Unemployment
  'JTSJOL', # Job Openings: Total Nonfarm
  'PAYEMS', # Non-Farm Employment
  'RSXFS', # Retail Sales
  'TCU', # Capacity Utilization
  'UMCSENT', # Consumer Sentiment Index
  'BUSINV', # Business Inventories
  'INDPRO', # Industrial Production Index
  'GACDFSA066MSFRBPHI', # Philidelphia Fed Manufacturing Index
  'GACDISA066MSFRBNY', # Empire State Manufacturing Index
  'BACTSAMFRBDAL', # Current General Business Activity; Diffusion Index for Texas
  'IR', # Import Price Index
  'IQ', # Export Price Index
  'PPIACO', # Producer Price Index - all
  'CPIAUCSL', # Consumer Price Index - all
  'CPILFESL', # Consumer Price Index (Core)
  'MICH', # University of Michigan: Inflation Expectation
  'CSCICP03USM665S', # Consumer Opinion Surveys: Confidence Indicators: Composite Indicators: OECD Indicator for the United States
]
macro_indicators = dict()
tq_fred = tqdm(report_list)
tq_fred.set_description('Downloading stats from FRED:')
idx = pd.date_range(start_date, end_date)
print(idx)
for indicator in tq_fred:
  # tq_fred.set_description(indicator)
  # macro_indicators[indicator] = pdr.DataReader(indicator, "fred", start=start, timeout=90)
  macro_indicators[indicator] = pdr.fred.FredReader(indicator, start=start_date, end = end_date, timeout=90).read()
  print(macro_indicators[indicator].index)
  macro_indicators[indicator] = macro_indicators[indicator].reindex(idx, fill_value=0).reset_index()
  print(macro_indicators[indicator])
  print(macro_indicators[indicator].columns.values)
  macro_indicators[indicator] = macro_indicators[indicator].rename(columns={"index": "Date"})
  macro_indicators[indicator][indicator] = macro_indicators[indicator][indicator].replace(to_replace=0, method='ffill')
  general_df = pd.merge(general_df, macro_indicators[indicator], how="left", on=['Date'])
  # print(macro_indicators[indicator])
general_df.to_csv('generated_df.csv')
print(general_df)