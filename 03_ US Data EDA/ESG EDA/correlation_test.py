import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns

esg_file_path = '/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/ESG/esg_data.csv'
esg_data = pd.read_csv(esg_file_path)

esg_data = esg_data.dropna(subset=[
    'Total ESG Risk score', 
    'Environment Risk Score', 
    'Social Risk Score', 
    'Governance Risk Score'
])

target = 'Total ESG Risk score'
esg_scores = ['Environment Risk Score', 'Social Risk Score', 'Governance Risk Score']

correlation_results = []

for score in esg_scores:
    pearson_corr, pearson_p = pearsonr(esg_data[score], esg_data[target])
    spearman_corr, spearman_p = spearmanr(esg_data[score], esg_data[target])
    correlation_results.append({
        'Feature': score,
        'Pearson Correlation': pearson_corr,
        'Pearson p-value': pearson_p,
        'Spearman Correlation': spearman_corr,
        'Spearman p-value': spearman_p
    })

correlation_df = pd.DataFrame(correlation_results)
print("Correlation Test Results:")
print(correlation_df)
