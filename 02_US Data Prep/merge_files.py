import pandas as pd
import re

def merge_esg_credit_data(matched_file, esg_file, credit_file, output_file):
    # Load the data
    matched_df = pd.read_csv(matched_file)
    esg_df = pd.read_csv(esg_file)
    credit_df = pd.read_csv(credit_file)
    
    # Standardize Company names in all files
    matched_df['Name'] = matched_df['Name']
    esg_df['Name'] = esg_df['Name']
    credit_df['Company'] = credit_df['Company']

    credit_df['Company'] = credit_df ['Company'].str.lower().str.strip()

    # Filter ESG and Credit data for matched companies
    common_df = pd.merge(credit_df, matched_df, left_on='Company', right_on='Company', how='inner').sort_values(['Date'], ascending=True)
                           
    combined_df = pd.merge(common_df, esg_df, left_on='Name', right_on='Name', how='inner').sort_values(['Date'], ascending=True)\
        .drop_duplicates(subset=['Name'], keep='last')

    combined_df.to_csv(output_file, index=False)
    print(f"Combined ESG and Credit data saved to {output_file}")

merge_esg_credit_data(
    '/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/DATA PREP/matched_ticked.csv',
    '/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/DATA PREP/esg_data.csv',
    '/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/DATA PREP/cleaned_credit_data.csv',
    '/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/DATA PREP/combined_esg_credit_data.csv'
)
