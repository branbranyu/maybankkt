import pandas as pd
import re
import numpy as np

input_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_social_counts.xlsx"
output_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_safety.xlsx"

df = pd.read_excel(input_path)
df = df.applymap(lambda x: str(x).replace(",", "") if isinstance(x, str) else x)

injury_cols = [
    "Number of fatalities as a result of work-related injury",
    "Number of high-consequence work-related injuries",
    "Number of recordable work-related injuries",
    "Number of recordable work-related ill health cases"
]

def extract_integer_counts(cell):
    if pd.isna(cell):
        return np.nan
    cell = str(cell).lower()
    if any(keyword in cell for keyword in [
        "rate", "trir", "dart", "per", "lost-time", "available", "not disclosed", "not specified", "%"
    ]):
        return np.nan
    matches = re.findall(r"\b\d+\b", cell)
    counts = [int(m) for m in matches if int(m) < 2020 or int(m) > 2026]
    if counts:
        return sum(counts)
    return np.nan

for col in injury_cols:
    if col in df.columns:
        df[col] = df[col].apply(extract_integer_counts).astype("Int64")

df.to_excel(output_path, index=False)
