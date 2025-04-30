import pandas as pd
import re

input_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_separated.xlsx"
output_path = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate/esg_metrics_converted.xlsx"

df = pd.read_excel(input_path)

# Step 1: Clean up commas and standardize text
df = df.applymap(lambda x: str(x).replace(",", "") if isinstance(x, str) else x)

# Step 2: Lowercase and strip all Unit columns
for col in df.columns:
    if col.endswith("Unit"):
        df[col] = df[col].astype(str).str.strip().str.lower()

# Step 3: Replace invalid placeholders in the entire DataFrame
df = df.applymap(lambda x: str(x).strip().lower() if isinstance(x, str) else x)
invalid_entries = {"not found", "not disclosed", "not reported", "unavailable"}
df.replace(invalid_entries, pd.NA, inplace=True)

# Step 4: Fuzzy unit standardization for Scope 1 & 2 Emissions
emissions_unit_map = {
    "tco2e": 1, "mt": 1e3, "mmt": 1e6, "kt": 1e3,
    "tons": 907.185, "tonnes": 1e3, "mtco2e": 1,
    "mtco": 1e3, "tco": 1, "co2e": 1
}

def standardize_fuzzy_units(metric_name, conversion_dict, standard_unit):
    val_col = f"{metric_name} Value"
    unit_col = f"{metric_name} Unit"

    def clean_and_convert(val, unit_text):
        try:
            val = float(val)
        except:
            return None, None
        unit_text = str(unit_text).lower()
        for raw_unit, multiplier in conversion_dict.items():
            if raw_unit in unit_text:
                return val * multiplier, standard_unit
        return None, None

    df[[val_col, unit_col]] = df[[val_col, unit_col]].apply(
        lambda row: pd.Series(clean_and_convert(row[val_col], row[unit_col])),
        axis=1
    )

standardize_fuzzy_units("Scope 1 Emissions", emissions_unit_map, "tco2e")
standardize_fuzzy_units("Scope 2 Emissions", emissions_unit_map, "tco2e")

# Step 5: Regular unit conversion for quantitative metrics
def standardize_metrics(metric_list, conversion_dict, standard_unit):
    for metric in metric_list:
        value_col = f"{metric} Value"
        unit_col = f"{metric} Unit"
        df[value_col] = df.apply(
            lambda row: row[value_col] * conversion_dict.get(row[unit_col], 1)
            if pd.notna(row[value_col]) and row[unit_col] in conversion_dict else None,
            axis=1
        )
        df[unit_col] = df[unit_col].apply(lambda x: standard_unit if x in conversion_dict else None)

litre_metrics = ["Fuel Consumption (Stationary Combustion)", "Fuel Consumption (Mobile Combustion)"]
litre_conversion = {
    "gj": 264.172, "twh": 1e12, "gwh": 1e9, "mwh": 1e6,
    "kwh": 1e3, "wh": 1, "l": 1, "litres": 1
}

m3_metrics = ["Water Consumption"]
m3_conversion = {
    "gallons": 0.00378541, "million gallons": 3785.41,
    "cubic meters": 1, "m³": 1, "m3": 1
}

kg_metrics = ["Waste Disposed (Non-hazardous)", "Waste Disposed (Hazardous)"]
kg_conversion = {
    "mt": 1e3, "metric tons": 1e3, "tons": 907.185, "kg": 1, "lbs": 0.453592
}

electricity_metrics = ["Electricity Consumption"]
electricity_conversion = {
    "kwh": 1, "mwh": 1e3, "gwh": 1e6, "twh": 1e9, "wh": 0.001
}

standardize_metrics(litre_metrics, litre_conversion, "litres")
standardize_metrics(m3_metrics, m3_conversion, "m³")
standardize_metrics(kg_metrics, kg_conversion, "kg")
standardize_metrics(electricity_metrics, electricity_conversion, "kwh")

# Step 6: Mark remaining Value/Unit columns as count-type
all_known_metrics = (
    litre_metrics + m3_metrics + kg_metrics +
    ["Scope 1 Emissions", "Scope 2 Emissions"] +
    electricity_metrics
)

all_known_value_cols = [f"{m} Value" for m in all_known_metrics]
value_cols_all = [col for col in df.columns if col.endswith("Value")]
unhandled_value_cols = [col for col in value_cols_all if col not in all_known_value_cols]

for val_col in unhandled_value_cols:
    unit_col = val_col.replace("Value", "Unit")
    if unit_col in df.columns:
        df[unit_col] = "count"
        df[val_col] = pd.to_numeric(df[val_col], errors="coerce")

# Step 7: Column order
columns_order = ["Company Name", "Company Symbol"] + [col for col in df.columns if col not in ["Company Name", "Company Symbol"]]
df = df[columns_order]

# Step 8: Save final result
df.to_excel(output_path, index=False)
