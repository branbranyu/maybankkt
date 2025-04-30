import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "/Users/branbranyu/Downloads/untitled folder/results.csv"
df = pd.read_csv(file_path)

# 1. Data Preparation
pillar_df = df[df['Pillar'].isin(['E', 'S', 'G'])].copy()
pillar_df['Coverage (%)'] = pd.to_numeric(pillar_df['Coverage (%)'], errors='coerce')

# 2. Stacked Bar Chart: Coverage by Company & Pillar
stacked_df = pillar_df.pivot_table(
    index='Company Name',
    columns='Pillar',
    values='Coverage (%)'
).fillna(0).sort_index()

stacked_df.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Coverage (%) by Company and ESG Pillar')
plt.ylabel('Coverage (%)')
plt.xlabel('Company')
plt.legend(title='Pillar')
plt.tight_layout()
plt.show()


# 3. Bar Chart: Average Coverage by Pillar
avg_coverage = pillar_df.groupby('Pillar')['Coverage (%)'].mean().round(1)

avg_coverage.plot(kind='bar', color='skyblue', figsize=(6, 4))
plt.title('Average Coverage (%) by ESG Pillar')
plt.ylabel('Average Coverage (%)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 4. Heatmap: Coverage by Company & Pillar
heatmap_df = pillar_df.pivot(
    index='Company Name',
    columns='Pillar',
    values='Coverage (%)'
)

plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_df, annot=True, cmap='YlGnBu', fmt='.1f', linewidths=0.5, linecolor='gray')
plt.title('Heatmap of ESG Coverage (%) by Company and Pillar')
plt.tight_layout()
plt.show()
