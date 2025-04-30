import pandas as pd
import os
import re

input_folder = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/01_raw"
output_folder = "/Users/branbranyu/Documents/Maybank/esg_extraction/data/02_intermediate"

all_data = []

for file in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file)
    if os.path.isfile(file_path) and file.endswith(".xlsx"):
        # Extract company name as the first word from the filename
        base_name = os.path.splitext(file)[0]
        company_match = re.match(r"^(.+)_Extracted_.*$", base_name)
        company_name = company_match.group(1) if company_match else "Unknown"

        try:
            df = pd.read_excel(file_path, engine="openpyxl")
        except Exception as e:
            print(f"Skipping file (error reading '{file}'): {e}")
            continue

        if "Metric Name" not in df.columns or "Extracted Value" not in df.columns:
            print(f"Skipping file (missing required columns): {file}")
            continue

        # Filter to include only 'Metric Name' and 'Extracted Value'
        filtered_df = df[["Metric Name", "Extracted Value"]]

        # Transpose the DataFrame
        transposed = filtered_df.set_index("Metric Name").T
        transposed.insert(0, "Company Name", company_name)

        all_data.append(transposed)

if all_data:
    combined_data = pd.concat(all_data, ignore_index=True)
    output_file = os.path.join(output_folder, "esg_metrics_transposed_combined.xlsx")
    combined_data.to_csv(output_file, index=False)
    print(f"Combined transposed data saved to: {output_file}")
else:
    print("No valid files found to process.")
