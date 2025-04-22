# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 14:20:35 2025

@author: 29301
"""

import pandas as pd

#Read the CSV files of financial statements from four companies
df_tesla_balance = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/tesla_balance.csv', index_col=0)
df_tesla_income = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/tesla_income.csv', index_col=0)
df_byd_balance = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/byd_balance.csv', index_col=0)
df_byd_income = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/byd_income.csv', index_col=0)
df_nio_balance = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/nio_balance.csv', index_col=0)
df_nio_income = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/nio_income.csv', index_col=0)
df_lucid_balance = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/lucid_balance.csv', index_col=0)
df_lucid_income = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/lucid_income.csv', index_col=0)
df_tesla_cash = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/tesla_cashflow.csv', index_col=0)
df_byd_cash = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/byd_cashflow.csv', index_col=0)
df_nio_cash = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/nio_cashflow.csv', index_col=0)
df_lucid_cash = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/lucid_cashflow.csv', index_col=0)

#Read ESG risk rating data
df_esg = pd.read_csv('C:/Users/29301/Desktop/Python/Group Work/EV_Companies_ESG_Scores.csv')

#Print the structure of ESG data
print(df_esg.head(4))

#Define the analysis year range (past 4 years)
years = [2020, 2021, 2022, 2023, 2024]
year_cols = [f"{y}-12-31" for y in years]

#Initialize the dictionary to save the data table for each ratio
ratio_names = ["ROE", "ROA", "NetMargin", "CurrentRatio", "QuickRatio", "DebtToAssets", "AssetTurnover"]
ratios = {name: pd.DataFrame(index=years, columns=["Tesla", "BYD", "NIO", "Lucid"], dtype=float) for name in ratio_names}

#Define a dictionary to store the corresponding balance sheet and income statement data frames for four companies, facilitating circular processing
companies_data = {
    'Tesla': (df_tesla_balance, df_tesla_income),
    'BYD': (df_byd_balance, df_byd_income),
    'NIO': (df_nio_balance, df_nio_income),
    'Lucid': (df_lucid_balance, df_lucid_income)
}
cashflow_data = {
    'Tesla': df_tesla_cash,
    'BYD': df_byd_cash,
    'NIO': df_nio_cash,
    'Lucid': df_lucid_cash
}


# Cash ratio needs Current Liabilities and Cash from balance sheet
cash_ratio_df = pd.DataFrame(index=years, columns=cashflow_data.keys())

for comp, df_cash in cashflow_data.items():
    # Debug output (optional)
    print(f"\\n--- {comp} ---")
    print("Cashflow Index Sample:", df_cash.index[:5])
    print("Balance Sheet Index Sample:", companies_data[comp][0].index[:5])

    # Cash Ratio = End Cash Position / Current Liabilities
    if "End Cash Position" in df_cash.index and "Current Liabilities" in companies_data[comp][0].index:
        cash = df_cash.loc["End Cash Position", df_cash.columns.intersection(year_cols)]
        curr_liab = companies_data[comp][0].loc["Current Liabilities", df_cash.columns.intersection(year_cols)]
        cash.index = cash.index.map(lambda x: int(x[:4]))
        curr_liab.index = curr_liab.index.map(lambda x: int(x[:4]))
        cash_ratio_df[comp] = cash / curr_liab


for comp, (df_bal, df_inc) in companies_data.items():
 #Extract the required subject data (if there is no data in a certain year, return NaN)
    net_income = df_inc.loc["Net Income", df_inc.columns.intersection(year_cols)]
    revenue = df_inc.loc["Total Revenue", df_inc.columns.intersection(year_cols)]
    equity = df_bal.loc["Stockholders Equity", df_bal.columns.intersection(year_cols)]
    total_assets = df_bal.loc["Total Assets", df_bal.columns.intersection(year_cols)]
    total_liab = df_bal.loc["Total Liabilities Net Minority Interest", df_bal.columns.intersection(year_cols)]
    curr_assets = df_bal.loc["Current Assets", df_bal.columns.intersection(year_cols)]
    curr_liab = df_bal.loc["Current Liabilities", df_bal.columns.intersection(year_cols)]
    inv = df_bal.loc["Inventory", df_bal.columns.intersection(year_cols)]
  #Convert the index to a year integer for easy alignment calculation by year
    for series in [net_income, revenue, equity, total_assets, total_liab, curr_assets, curr_liab, inv]:
        series.index = series.index.map(lambda x: int(x[:4]))
#Calculate various ratios and store them in the corresponding DataFrame
    ratios['ROE'][comp] = net_income / equity
    ratios['ROA'][comp] = net_income / total_assets
    ratios['NetMargin'][comp] = net_income / revenue
    ratios['CurrentRatio'][comp] = curr_assets / curr_liab
    ratios['QuickRatio'][comp] = (curr_assets - inv) / curr_liab
    ratios['DebtToAssets'][comp] = total_liab / total_assets
    ratios['AssetTurnover'][comp] = revenue / total_assets

#Dispaly calculation results (rounded to 2 decimal places)
print("ROE (%) for 2021-2023:\n", (ratios['ROE'].loc[2021:2023] * 100).round(2))

import numpy as np

#Using linear regression to predict ratio values for the next two years
for comp in ["Tesla", "BYD", "NIO", "Lucid"]:
    for name in ratio_names:
  #Extract the years and values of actual data available for the company
        known = ratios[name][comp].dropna()
        if len(known) >= 2:
            x = np.array(known.index, dtype=float)
            y = known.values.astype(float)
         #Fit a linear model y=a * x+b
            a, b = np.polyfit(x, y, 1)
         #Predict the next year until 2026
            last_year = known.index.max()
            for fut_year in [2025, 2026]:
                if fut_year > last_year:
                    ratios[name].at[fut_year, comp] = a * fut_year + b

import matplotlib.pyplot as plt

plt.style.use('ggplot')  #Beautify chart style

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

for name in ratio_names:
    plt.figure(figsize=(10, 6))
    for comp in ["Tesla", "BYD", "NIO", "Lucid"]:
      #Extract data
        series = ratios[name][comp].sort_index()
        years = series.index
        values = series.values
     #Draw the solid line section
        split_idx = (years <= 2024)
        plt.plot(years[split_idx], values[split_idx], label=f'{comp} (actuality)', linewidth=2)
       #Draw the prediction section (dashed line)
        if any(years > 2024):
            plt.plot(years[years > 2024], values[years > 2024], linestyle='--', label=f'{comp} (prediction)')
    plt.title(f'{name} Trend chart (including forecast)')
    plt.xlabel("Year")
    plt.ylabel(name)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Draw Cash Ratio trend
cash_ratio_df = cash_ratio_df.astype(float)
cash_ratio_df.plot(marker='o', figsize=(10,6), title="Cash Ratio Trend")
plt.xlabel("Year")
plt.ylabel("Cash Ratio")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

#Consistent order of ESG data set for companies
companies = ["Tesla", "BYD", "NIO", "Lucid"]
esg_env = df_esg.set_index("Company").loc[companies]["Environmental Risk Score"]
esg_soc = df_esg.set_index("Company").loc[companies]["Social Risk Score"]
esg_gov = df_esg.set_index("Company").loc[companies]["Governance Risk Score"]

x = range(len(companies))
width = 0.25

plt.figure(figsize=(10,6))
plt.bar([p - width for p in x], esg_env, width=width, label="Environmental risk", color='green')
plt.bar(x, esg_soc, width=width, label="Social risk", color='orange')
plt.bar([p + width for p in x], esg_gov, width=width, label="Governance Risk", color='purple')

plt.xticks(x, companies)
plt.ylabel("risk score")
plt.title("Comparison of ESG risk ratings among companies")
plt.legend()
plt.tight_layout()
plt.show()

esg_total = df_esg.set_index("Company").loc[companies]["Total ESG Risk Score"]
roa_2023 = ratios['ROA'].loc[2023, companies] * 100  #Convert to percentage

plt.figure(figsize=(8,6))
for comp in companies:
    plt.scatter(esg_total[comp], roa_2023[comp], label=comp, s=100)
    plt.text(esg_total[comp]+0.3, roa_2023[comp], comp)

plt.xlabel("ESG Total risk score (the lower the better)")
plt.ylabel("ROA in 2023 (%)")
plt.title("ESG Risk vs Financial Profitability")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

print("- Summary of Analysis:")
print("- Tesla: Tesla has the strongest profitability (stable ROA and ROE) and a moderate cash ratio that, while declining from around 0.9 to 0.6 over the past few years, still suggests adequate short-term liquidity. ESG performance is also strong, with Tesla achieving the lowest environmental risk score.")
print("- BYD: BYD’s financial performance has improved rapidly, but its cash ratio remains very low (around 0.2), indicating weak cash coverage of short-term liabilities. This low liquidity, coupled with relatively high ESG risk (especially environmental) and a high debt load, could pose near-term financial stability concerns.")
print("- NIO: NIO continues to operate at a loss (negative ROA and ROE), reflecting ongoing profitability pressures. Its cash ratio has plummeted from over 2 in 2020 to roughly 0.6 in 2023, significantly eroding the company’s cash cushion and raising potential liquidity risks. Additionally, NIO’s ESG risk remains relatively high.")
print("- Lucid: Lucid has the lowest ESG risk score but the worst financial performance of the group. Its cash ratio – although still above 1 (meaning cash exceeds current liabilities) – plunged from about 15 in 2021 to ~1.3 in 2023, reflecting heavy cash burn and rapidly depleting initial funds. There is an urgent need for Lucid to rein in cash outflows and boost revenue to prevent future liquidity issues.")
