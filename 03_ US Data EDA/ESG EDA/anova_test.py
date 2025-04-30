import pandas as pd
import numpy as np
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
import seaborn as sns

# Load the ESG data
esg_file_path = '/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/ESG/esg_data.csv'
esg_data = pd.read_csv(esg_file_path)

# Drop rows with NaN values in 'Total ESG Risk Score'
esg_data = esg_data.dropna(subset=['Total ESG Risk score'])

target = 'Total ESG Risk score'
features = [col for col in esg_data.columns if col != target]

# Filter numeric features for ANOVA analysis
numeric_features = esg_data[features].select_dtypes(include=[np.number]).columns.tolist()

# Perform ANOVA on each numerical feature by binning them
anova_results = {}
for feature in numeric_features:
    # Bin the numerical feature into quartiles
    esg_data[feature+'_bin'] = pd.qcut(esg_data[feature], q=4, duplicates='drop')

    groups = [esg_data[esg_data[feature+'_bin'] == cat][target] for cat in esg_data[feature+'_bin'].unique()]
    f_stat, p_value = f_oneway(*groups)

    anova_results[feature] = {'F-statistic': f_stat, 'p-value': p_value}

anova_df = pd.DataFrame(anova_results).T
anova_df = anova_df.sort_values(by='p-value')
print("ANOVA Test Results:")
print(anova_df)
