# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 14:07:07 2025

@author: 29301
"""
import yfinance as yf


tsla = yf.Ticker("TSLA")

income_stmt = tsla.financials
print(income_stmt)
balance_sheet = tsla.balance_sheet
print(balance_sheet)
cash_flow = tsla.cashflow
print(cash_flow)
info = tsla.info


income_stmt.to_csv("tesla_income.csv")
balance_sheet.to_csv("tesla_balance.csv")
cash_flow.to_csv("tesla_cashflow.csv")

