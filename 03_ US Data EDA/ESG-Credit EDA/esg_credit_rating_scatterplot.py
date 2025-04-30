import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

file_path = "/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/CREDIT-ESG/combined_data.csv"
data = pd.read_csv(file_path)

rating_mapping = {
    'AAA': 1, 'AA+': 2, 'AA': 3, 'AA-': 4,
    'A+': 5, 'A': 6, 'A-': 7,
    'BBB+': 8, 'BBB': 9, 'BBB-': 10,
    'BB+': 11, 'BB': 12, 'BB-': 13,
    'B+': 14, 'B': 15, 'B-': 16,
    'CCC+': 17, 'CCC': 18, 'CCC-': 19,
    'CC': 20, 'C': 21, 'D': 22
}

data['Numerical Rating'] = data['Rating'].map(rating_mapping)

data = data.dropna(subset=[
    'Total ESG Risk score', 
    'Environment Risk Score', 
    'Social Risk Score', 
    'Governance Risk Score',
    'Numerical Rating'
])

output = "/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/CREDIT-ESG/combined_data.csv"
data.to_csv(output, index=False)
print(f"Updated file saved as: {output}")

esg_features = ['Total ESG Risk score', 'Environment Risk Score', 'Social Risk Score', 'Governance Risk Score']
r2_scores = {}

plt.figure(figsize=(20, 10))
plt.suptitle('Scatter Plots and R-Squared Values of ESG Scores vs Credit Rating', fontsize=16)

for i, feature in enumerate(esg_features):
    plt.subplot(2, 2, i+1)
    sns.regplot(x=feature, y='Numerical Rating', data=data, scatter_kws={'alpha':0.6}, line_kws={'color':'red'})
    plt.title(f'{feature} vs Numerical Rating')
    plt.xlabel(feature)
    plt.ylabel('Numerical Rating')
    plt.grid(True)

    X = data[[feature]].values
    y = data['Numerical Rating'].values
    model = LinearRegression().fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    r2_scores[feature] = r2
    
    plt.text(0.05, 0.95, f'R² = {r2:.3f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

print("R-squared Values for ESG Scores vs Numerical Rating:")
for feature, r2 in r2_scores.items():
    print(f"{feature}: R² = {r2:.3f}")
