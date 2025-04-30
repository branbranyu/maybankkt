import pandas as pd
import re

input_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_transposed_combined_symbols.xlsx"
output_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_separated.xlsx"

df = pd.read_excel(input_path)

# Remove commas
df = df.applymap(lambda x: str(x).replace(",", "") if isinstance(x, str) else x)

# Metrics to process
metrics = [
    "Fuel Consumption (Mobile Combustion)",
    "Fuel Consumption (Stationary Combustion)",
    "Electricity Consumption",
    "Water Consumption",
    "Waste Disposed (Non-hazardous)",
    "Waste Disposed (Hazardous)",
    "Scope 1 Emissions",
    "Scope 2 Emissions",
    "Emissions Intensity"
]

# Define scale word multipliers
scale_map = {
    "thousand": 1e3,
    "million": 1e6,
    "billion": 1e9
}

# Save original column order
original_cols = df.columns.tolist()
replacement_cols = {}

# Process each metric
for metric in metrics:
    value_col = f"{metric} Value"
    unit_col = f"{metric} Unit"

    # Extract numeric part
    df[value_col] = df[metric].str.extract(r"([-+]?\d*\.?\d+)", expand=False)
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    # Extract and apply scale word multiplier inline
    scale_word = df[metric].str.extract(r"\b(thousand|million|billion)\b", expand=False)
    df[value_col] *= scale_word.map(scale_map).fillna(1)

    # Extract clean unit
    df[unit_col] = df[metric].str.extract(r"\d[\d,.]*\s*(?:thousand|million|billion)?\s*([a-zA-Zµ/%²³]+)", expand=False)
    replacement_cols[metric] = [value_col, unit_col]

# Preserve original columns
new_cols = []
for col in original_cols:
    if col in replacement_cols:
        new_cols.extend(replacement_cols[col])
    else:
        new_cols.append(col)

df.drop(columns=metrics, inplace=True)
df = df[new_cols]

df.to_excel(output_path, index=False)
