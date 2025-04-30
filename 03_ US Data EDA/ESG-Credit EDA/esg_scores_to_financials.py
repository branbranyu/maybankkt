import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

print("Numpy version:", np.__version__)
print("Pandas version:", pd.__version__)

# Load your data
data = pd.read_csv("/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/250325 UPDATE/combined_data.csv")

# Financial and ESG columns
financial_columns = [
    "Current Ratio", "Long-term Debt / Capital", "Debt/Equity Ratio", 
    "Gross Margin", "Operating Margin", "EBIT Margin", "EBITDA Margin", 
    "Pre-Tax Profit Margin", "Net Profit Margin", "Asset Turnover", 
    "ROE - Return On Equity", "Return On Tangible Equity", "ROA - Return On Assets", 
    "ROI - Return On Investment", "Operating Cash Flow Per Share", "Free Cash Flow Per Share"
]

esg_columns = [
    "Environment Risk Score", "Social Risk Score", 
    "Governance Risk Score", "Total ESG Risk score"
]

# Filter and compute correlation
correlation_data = data[financial_columns + esg_columns]

# calculate correlation used spearman method
correlation_matrix = correlation_data.corr(method='spearman')

# --------- 📊 Enhanced Heatmap Plot (Improved Readability) ---------
plt.figure(figsize=(18, 10))
heatmap = sns.heatmap(
    correlation_matrix.loc[esg_columns, financial_columns], 
    annot=True, cmap="coolwarm", fmt=".2f", 
    annot_kws={"size": 14},  # Increase font size for annotation numbers
    linewidths=0.5, linecolor='grey',
    vmin=-1, vmax=1
)
plt.xticks(rotation=45, ha='right', fontsize=14, weight='bold')  # Increase font size for x-axis labels
plt.yticks(rotation=0, fontsize=14, weight='bold')  # Increase font size for y-axis labels
plt.title("Correlation of Financials with ESG Scores", fontsize=18, weight='bold', pad=20)  # Increase title font size
plt.tight_layout()
plt.show()

# --------- 🔍 Identify Strong Correlations ---------
threshold = 0.3
strong_pairs = []

for esg in esg_columns:
    for fin in financial_columns:
        corr = correlation_matrix.at[esg, fin]
        if abs(corr) > threshold:
            strong_pairs.append((esg, fin, corr))

strong_pairs.sort(key=lambda x: abs(x[2]), reverse=True)

# --------- 📈 Scatter & Heatmap Plots for Strong Pairs ---------
for esg, fin, corr in strong_pairs:
    # Scatterplot
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=data, x=fin, y=esg)
    plt.title(f"Scatterplot: {fin} vs {esg} (r={corr:.2f})")
    plt.xlabel(fin)
    plt.ylabel(esg)
    plt.tight_layout()
    plt.show()

    # Binned heatmap
    plt.figure(figsize=(8, 6))
    sns.histplot(data=data, x=fin, y=esg, bins=30, cbar=True, cmap="viridis")
    plt.title(f"Binned Heatmap: {fin} vs {esg} (r={corr:.2f})")
    plt.xlabel(fin)
    plt.ylabel(esg)
    plt.tight_layout()
    plt.show()
