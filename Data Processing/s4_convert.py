import pandas as pd
import re
import numpy as np

input_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_training.xlsx"
output_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_board.xlsx"
df = pd.read_excel(input_path)

board_cols = [
    "Number of Independent Board Directors",
    "Number of Women on the Board of Directors"
]

def extract_board_count(text):
    if pd.isna(text):
        return np.nan
    text = str(text).lower()

    if any(kw in text for kw in ["not specified", "not explicitly", "not directly", "unspecified", "unknown", "majority", "composed of"]):
        return np.nan

    # Discard values that contain % but no total (like "42%")
    if "%" in text and not re.search(r"\d+\s+of\s+\d+", text):
        return np.nan

    match_of = re.search(r"\b(\d+)\s+of\s+\d+", text)
    if match_of:
        return int(match_of.group(1))

    match_paren = re.search(r"\b(\d+)\s*\(\s*\d+%.*?\)", text)
    if match_paren:
        return int(match_paren.group(1))

    match_out_of = re.search(r"\b(\d+)\s+women?", text)
    if match_out_of:
        return int(match_out_of.group(1))

    match_simple = re.search(r"\b(\d+)\b", text)
    if match_simple:
        return int(match_simple.group(1))

    return np.nan

for col in board_cols:
    if col in df.columns:
        df[col] = df[col].apply(extract_board_count).astype("Int64")

df.to_excel(output_path, index=False)
