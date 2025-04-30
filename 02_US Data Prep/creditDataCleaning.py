import pandas as pd
import re
from rapidfuzz import process, fuzz

def standardize_company_name(name):
    """
    Standardizes company names by:
    - Lowercasing and stripping whitespace
    - Removing special characters (commas, periods, hyphens)
    - Removing common suffixes like Inc, Corp, LLC, Ltd
    """
    if pd.isna(name):
        return name
    
    # Convert to lowercase and strip whitespace
    name = name.lower().strip()
    
    # Remove special characters
    name = re.sub(r'[.,\-]', '', name)
    
    # Remove common suffixes
    name = re.sub(r'\b(inc|corp|corporation|llc|ltd|limited|plc|co|group|holdings|company)\b', '', name)
    
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name)
    
    return name

def fuzzy_match_names(df, threshold=85):
    """
    Groups similar company names using fuzzy matching.
    Only retains one name per group (most frequent one).
    """
    unique_names = df['Company'].unique()
    matched_names = {}
    
    for name in unique_names:
        # Skip already matched names
        if name in matched_names:
            continue
        
        # Find matches above the threshold
        matches = process.extract(name, unique_names, scorer=fuzz.ratio)
        similar_names = [match[0] for match in matches if match[1] >= threshold]
        
        # Assign the most common name to all similar ones
        primary_name = max(similar_names, key=lambda x: (df['Company'] == x).sum())
        for n in similar_names:
            matched_names[n] = primary_name
    
    # Replace names with their matched group
    df['Company'] = df['Company'].map(matched_names)
    return df

def creditDataCleaning(input, output):
    # Load the data
    df = pd.read_csv(input)
    
    # Rename columns for consistency
    df.rename(columns={'Corporation': 'Company', 'Rating Date': 'Date'}, inplace=True)

    # Check for required columns
    requiredColumns = ['Company', 'Date']
    missingColumns = [col for col in requiredColumns if col not in df.columns]
    if missingColumns:
        raise KeyError(f"Missing columns: {missingColumns}")
    
    # Convert Date column to datetime format and remove rows with invalid dates
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    
    # Standardize Company names
    df['Company'] = df['Company']

    # Filter to keep only the latest recorded data per company (regardless of Rating Agency)
    df = df.sort_values(by='Date', ascending=False).drop_duplicates(subset=['Company'], keep='first')

    # Identify numerical columns for outlier removal
    numericalColumns = df.select_dtypes(include=['number']).columns

    # Save the cleaned data to a new CSV file
    df.to_csv(output, index=False)
    print(f"Cleaned data saved to {output}")

# Usage
creditDataCleaning(
    '/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/DATA PREP/credit_data.csv',
    '/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/DATA PREP/cleaned_credit_data.csv'
)
