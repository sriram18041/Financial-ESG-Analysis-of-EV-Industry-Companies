# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 14:18:48 2025

@author: 29301
"""

import yfinance as yf


byd = yf.Ticker("1211.HK")  


income_stmt = byd.financials
print(income_stmt)

balance_sheet = byd.balance_sheet
print(balance_sheet)

cash_flow = byd.cashflow
print(cash_flow)

info = byd.info  


income_stmt.to_csv("byd_income.csv")
balance_sheet.to_csv("byd_balance.csv")
cash_flow.to_csv("byd_cashflow.csv")