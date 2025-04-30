import pandas as pd
import re
import numpy as np

input_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_safety.xlsx"
output_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_training.xlsx"
df = pd.read_excel(input_path)

training_cols = [
    "Average training hours per employee",
    "Average training hours per male employee",
    "Average training hours per female employee"
]

def clean_training_hours(cell):
    if pd.isna(cell):
        return np.nan

    text = str(cell).lower()

    if any(kw in text for kw in [
        "not specified", "not separately", "not quantified", "omitted", "unspecified", "unknown"
    ]):
        return np.nan

    match_div = re.search(r"([\d\.,]+)\s*(million|thousand)?[^/]+/[^/]+([\d\.,]+)", text)
    if match_div:
        num = float(match_div.group(1).replace(",", ""))
        denom = float(match_div.group(3).replace(",", ""))
        multiplier = {"million": 1e6, "thousand": 1e3}.get(match_div.group(2), 1)
        avg = num * multiplier / denom
        return round(avg, 1) if avg < 1000 else np.nan

    match = re.search(r"\b(\d+(\.\d+)?)\b", text)
    if match:
        val = float(match.group(1))
        return val if val < 1000 else np.nan

    return np.nan

for col in training_cols:
    if col in df.columns:
        df[col] = df[col].apply(clean_training_hours)

df[training_cols] = df[training_cols].astype(float).round(1)

df.to_excel(output_path, index=False)
