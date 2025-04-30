import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway, spearmanr, pearsonr
from sklearn.preprocessing import LabelEncoder

# Load the combined ESG and Credit Rating data
file_path = "/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/CREDIT-ESG/combined_data.csv"
data = pd.read_csv(file_path)

# Group Ratings into Bands
rating_bands = {
    'AAA': 'Band 1', 
    'AA+': 'Band 2', 'AA': 'Band 2', 'AA-': 'Band 2',
    'A+': 'Band 3', 'A': 'Band 3', 'A-': 'Band 3',
    'BBB+': 'Band 4', 'BBB': 'Band 4', 'BBB-': 'Band 4',
    'BB+': 'Band 5', 'BB': 'Band 5', 'BB-': 'Band 5',
    'B+': 'Band 6', 'B': 'Band 6', 'B-': 'Band 6',
    'CCC+': 'Very Low Grade', 'CCC': 'Very Low Grade', 'CCC-': 'Very Low Grade',
    'CC': 'Very Low Grade', 'C': 'Very Low Grade', 'D': 'Very Low Grade'
}

# Add a Rating Band Column
data['Rating Band'] = data['Rating'].map(rating_bands)

# Drop rows with NaN values in relevant columns
data = data.dropna(subset=[
    'Total ESG Risk score', 
    'Environment Risk Score', 
    'Social Risk Score', 
    'Governance Risk Score',
    'Rating Band'
])

# Encode Credit Rating Bands for Correlation Analysis
label_encoder = LabelEncoder()
data['Encoded Rating Band'] = label_encoder.fit_transform(data['Rating Band'])

# Save the updated file
output_file = "/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/CREDIT-ESG/combined_data_with_bands.csv"
data.to_csv(output_file, index=False)
print(f"Updated file saved as: {output_file}")

# Define the order of Rating Bands for consistent plotting (Excluding Very Low Grade)
rating_order = ['Band 1', 'Band 2', 'Band 3', 'Band 4', 'Band 5', 'Band 6']

# Filter out Very Low Grade for Boxplots and Scatter Plots
data_filtered = data[data['Rating Band'] != 'Very Low Grade']

# Features to Analyze
esg_features = ['Total ESG Risk score', 'Environment Risk Score', 'Social Risk Score', 'Governance Risk Score']

# ----- 1. ANOVA Test -----
print("\nANOVA Test Results:")
anova_results = {}
for feature in esg_features:
    groups = [data[data['Rating Band'] == band][feature] for band in rating_order]
    f_stat, p_value = f_oneway(*groups)
    anova_results[feature] = {'F-statistic': f_stat, 'p-value': p_value}
    print(f"{feature} - F-statistic: {f_stat:.3f}, p-value: {p_value:.3e}")

# ----- 2. Correlation Analysis ------
print("\nCorrelation Analysis with Encoded Credit Rating Bands:")
correlation_results = {}
for feature in esg_features:
    pearson_corr, pearson_p = pearsonr(data[feature], data['Encoded Rating Band'])
    spearman_corr, spearman_p = spearmanr(data[feature], data['Encoded Rating Band'])

    correlation_results[feature] = {
        'Pearson Correlation': pearson_corr,
        'Pearson p-value': pearson_p,
        'Spearman Correlation': spearman_corr,
        'Spearman p-value': spearman_p
    }

    print(f"{feature} - Pearson: {pearson_corr:.3f}, p-value: {pearson_p:.3e}")
    print(f"           Spearman: {spearman_corr:.3f}, p-value: {spearman_p:.3e}")

# ----- 3. Boxplots to Compare Distributions -----
plt.figure(figsize=(18, 10))
plt.suptitle('Boxplots of ESG Scores by Credit Rating Band', fontsize=16)

for i, feature in enumerate(esg_features):
    plt.subplot(2, 2, i+1)
    sns.boxplot(x='Rating Band', y=feature, data=data_filtered, palette='Set2', order=rating_order)
    plt.title(f'{feature} by Credit Rating Band')
    plt.xlabel('Rating Band')
    plt.ylabel(feature)
    plt.grid(True)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

# ------ 4. Scatter Plots ------
plt.figure(figsize=(20, 10))
plt.suptitle('Scatter Plots of ESG Scores vs Credit Rating Band', fontsize=16)

for i, feature in enumerate(esg_features):
    plt.subplot(2, 2, i+1)
    sns.stripplot(x='Rating Band', y=feature, data=data_filtered, jitter=True, palette='Set1', order=rating_order)
    plt.title(f'{feature} vs Rating Band')
    plt.xlabel('Rating Band')
    plt.ylabel(feature)
    plt.grid(True)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
