import pandas as pd
import re
import numpy as np

input_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_converted.xlsx"
output_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_social_counts.xlsx"

df = pd.read_excel(input_path)
df = df.applymap(lambda x: str(x).replace(",", "") if isinstance(x, str) else x)

# === Columns to clean ===
demographic_cols = [
    "Current Employee by Age Group - Under 30 years old",
    "Current Employee by Age Group - 30-50 years old",
    "Current Employee by Age Group - Over 50 years old",
    "Current Employee by Age Group - Male",
    "Current Employee by Age Group - Female"
]

new_hire_cols = [
    "Total number of new employees hires during the reporting period, by age group - Under 30 years old",
    "Total number of new employees hires during the reporting period, by age group - 30-50 years old",
    "Total number of new employees hires during the reporting period, by age group - Over 50 years old",
    "Total number of new employees hires during the reporting period, by age group - Male",
    "Total number of new employees hires during the reporting period, by age group - Female"
]

total_col = "Total Number of Current Employees"

# === Step 1: Clean total employees column ===
def parse_total(val):
    if pd.isna(val):
        return np.nan
    val = str(val).lower()
    if "million" in val:
        match = re.search(r"([\d\.]+)", val)
        return float(match.group(1)) * 1_000_000 if match else np.nan
    match = re.search(r"(\d+)", val.replace("+", ""))
    return float(match.group(1)) if match else np.nan

df[total_col] = df[total_col].apply(parse_total)

# === Step 2: Clean and convert demographic cells to numeric counts ===
def clean_and_convert(cell, total_employees):
    if pd.isna(cell):
        return np.nan
    original = str(cell).lower()
    cleaned = re.sub(r"[^\d.%]", " ", original)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if "%" in cleaned:
        match = re.search(r"([\d\.]+)", cleaned)
        if match and pd.notna(total_employees):
            pct = float(match.group(1)) / 100
            return round(pct * total_employees)
    if re.fullmatch(r"0\.\d+", cleaned) and pd.notna(total_employees):
        return round(float(cleaned) * total_employees)
    match_count = re.search(r"(\d+(\.\d+)?)", cleaned)
    if match_count:
        return float(match_count.group(1))
    return np.nan

for col in demographic_cols:
    df[col] = df.apply(lambda row: clean_and_convert(row[col], row[total_col]), axis=1)

# === Step 3: Remove %/proportions from new hire columns ===
def remove_percent_or_proportion(val):
    if pd.isna(val):
        return np.nan
    val_str = str(val).lower()
    val_str = re.sub(r"[^\d.%]", "", val_str)
    if "%" in val_str or re.fullmatch(r"0\.\d+", val_str):
        return np.nan
    match = re.search(r"\d+(\.\d+)?", val_str)
    return float(match.group(0)) if match else np.nan

for col in new_hire_cols:
    if col in df.columns:
        df[col] = df[col].apply(remove_percent_or_proportion)

# === Step 4: Drop %/proportion demographic values if total missing
for col in demographic_cols:
    def drop_if_missing_total(val, total):
        val_str = str(val).lower()
        if pd.isna(total):
            if "%" in val_str or re.fullmatch(r"0\.\d+", val_str):
                return np.nan
        return val
    df[col] = df.apply(lambda row: drop_if_missing_total(row[col], row[total_col]), axis=1)

# === Step 5: Convert demographic and new hire columns to integers (whole numbers)
for col in demographic_cols + new_hire_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").round(0).astype("Int64")

df.to_excel(output_path, index=False)
