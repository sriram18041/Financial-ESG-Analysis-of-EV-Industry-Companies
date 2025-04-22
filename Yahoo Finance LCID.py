# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 14:19:54 2025

@author: 29301
"""

import yfinance as yf
import pandas as pd


lcid = yf.Ticker("LCID")


income_stmt = lcid.financials
print(income_stmt)

balance_sheet = lcid.balance_sheet
print(balance_sheet)

cash_flow = lcid.cashflow
print(cash_flow)

info = lcid.info

income_stmt.to_csv("lucid_income.csv")
balance_sheet.to_csv("lucid_balance.csv")
cash_flow.to_csv("lucid_cashflow.csv")
