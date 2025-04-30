import pandas as pd

combined_data_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/03_final/combined_data.csv"
metrics_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/03_final/esg_metrics_final.xlsx"
output_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/03_final/esg_metrics_final_scores.xlsx"

combined_df = pd.read_csv(combined_data_path)
metrics_df = pd.read_excel(metrics_path)

combined_df['Ticker'] = combined_df['Ticker'].str.lower()
metrics_df['Company Symbol'] = metrics_df['Company Symbol'].str.lower()

score_cols = [
    'Ticker',
    'Total ESG Risk score',
    'Environment Risk Score',
    'Social Risk Score',
    'Governance Risk Score'
]
score_df = combined_df[score_cols]
merged_df = metrics_df.merge(score_df, how='left', left_on='Company Symbol', right_on='Ticker')
merged_df.drop(columns=['Ticker'], inplace=True)

merged_df.to_excel(output_path, index=False)
