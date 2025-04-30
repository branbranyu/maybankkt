import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/ESG ANALYSIS/combined_data.csv")

esg_bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
esg_labels = [f'{i}-{i+5}' for i in range(0, 100, 5)]
df['ESG_bands'] = pd.cut(df['Total ESG Risk score'], bins=esg_bins, labels=esg_labels)

credit_bins = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 25]
credit_labels = [f'{credit_bins[i]}-{credit_bins[i+1]}' for i in range(len(credit_bins) - 1)]
df['Credit_bands'] = pd.cut(df['Numerical Rating'], bins=credit_bins, labels=credit_labels)

table = pd.crosstab(df['ESG_bands'], df['Credit_bands'])

plt.figure(figsize=(14, 8))
sns.heatmap(
    table, 
    annot=True, 
    fmt='d', 
    cmap='Blues', 
    linewidths=0.5, 
    annot_kws={"size": 16}
)
plt.title('ESG vs Credit Rating Distribution', fontsize=20, weight='bold')
plt.xlabel('Credit Rating', fontsize=18, weight='bold')
plt.ylabel('ESG Risk Score', fontsize=18, weight='bold')
plt.xticks(rotation=45, fontsize=16, weight='bold')
plt.yticks(rotation=0, fontsize=16, weight='bold')
plt.tight_layout()
plt.show()

table.to_csv('esg_credit_distribution.csv')
