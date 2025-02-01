import pandas as pd
import re

# Define replacement rules
REPLACEMENT_RULES = {
    r'\bCarrera\b': 'CR',
    r'\bCalle\b': 'CL',
    r'\bZona franca\b': 'ZF',
    # Add more rules as needed
}

def preprocess_addresses(df, address_column):
    # Apply replacement rules
    for pattern, replacement in REPLACEMENT_RULES.items():
        df[address_column] = df[address_column].str.replace(pattern, replacement, regex=True, case=False)
    
    # Handle missing values
    df[address_column] = df[address_column].fillna('').str.strip()
    
    return df

def load_and_preprocess(input_csv, output_csv):
    # Load the CSV file
    df = pd.read_csv(input_csv)
    
    # Identify the address column (case insensitive)
    address_column = next((col for col in df.columns if 'address' in col.lower()), None)
    if not address_column:
        raise ValueError("No address column found in the dataset.")
    
    # Preprocess addresses
    df = preprocess_addresses(df, address_column)
    
    # Save the processed data to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Preprocessed data saved to {output_csv}")

# Example usage
input_csv = 'address_data.csv'
output_csv = 'preprocessed_addresses.csv'
load_and_preprocess(input_csv, output_csv)