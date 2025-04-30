import pandas as pd
from fuzzywuzzy import process, fuzz

credit_data_path = '/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/DATA PREP/cleaned_credit_data.csv'
esg_data_path = '/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/DATA PREP/esg_data.csv'
credit_data = pd.read_csv(credit_data_path)
esg_data = pd.read_csv(esg_data_path)

# ---- Convert all names to lowercase ----
credit_data["Company"] = credit_data["Company"].str.lower()
esg_data["Name"] = esg_data["Name"].str.lower()

credit_column = 'Company'
esg_column = 'Name'

credit_data[credit_column] = credit_data [credit_column].str.lower().str.strip()
esg_data[esg_column] = esg_data[esg_column].str.lower().str.strip()

# ---- Create a list of ESG company names for matching ----
esg_companies_list = esg_data[esg_column].tolist()

# ---- Find best matches using Levenshtein distance ----
matches = []
for credit_company in credit_data[credit_column]:
    best_match, score = process.extractOne(credit_company, esg_companies_list, scorer = fuzz.ratio)
    matches.append([credit_company, best_match, score])

matches_df = pd.DataFrame(matches, columns = ["Company", "Name", "Score"]).sort_values(by = "Score", ascending = False)
matches_df.to_csv('/Users/branbranyu/Documents/Maybank/Sustainability Use Case/EDA/DATA PREP/matches.csv', index = False)

