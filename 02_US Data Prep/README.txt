Objective:
To combine ESG data and Credit data into one combined file for analysis.

Input: 
- Credit Data: credit_data.csv
- ESG Data: esg_data.csv

Pipeline:
1. creditDataCleaning.py
- Renames columns (Corporation → Company, Rating Date → Date) for consistency.
- Validates that key columns (Company, Date) exist in the dataset.
- Standardises the Date format and removes rows with invalid dates. 
- Standardises company names by lowercasing, removing special characters and common corporate suffixes (function is defined but not applied yet).

Output: cleaned_credit_data.csv

(Note: there was not any data cleaning for the ESG data, as it was preprocessed from the Kaggle dataset)

2. match_companies.py
- Standardises company names by  converting all names in both datasets to lowercase and strips whitespace.
- Prepares a list of ESG company names for matching.
- Performs fuzzy matching, by calculating the Levenshtein distance (via FuzzyWuzzy) to find the best match from the ESG dataset. Captures both the matched ESG company name and the similarity score.

Output: matches.csv

3. Manual matching:
- Went through the pairs of matched companies and confirmed the correctly matched companies.

Output: matched_ticked.csv

4. merge_files.py
- Fetched the company data from both ESG and credit dataset.

Output: combined_esg_credit_data.csv

