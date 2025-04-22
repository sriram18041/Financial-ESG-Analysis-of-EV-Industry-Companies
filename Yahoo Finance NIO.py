# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 14:19:39 2025

@author: 29301
"""

import yfinance as yf
import pandas as pd


nio = yf.Ticker("NIO")


income_stmt = nio.financials
print(income_stmt)

balance_sheet = nio.balance_sheet
print(balance_sheet)

cash_flow = nio.cashflow
print(cash_flow)

info = nio.info  


income_stmt.to_csv("nio_income.csv")
balance_sheet.to_csv("nio_balance.csv")
cash_flow.to_csv("nio_cashflow.csv")
