import time
import pandas as pd
import ollama
from requests.exceptions import ConnectionError  # Correct import

def standardize_address_with_llm(address):
    try:
        response = ollama.generate(
            model='deepseek-r1:7b',  # Use EXACT model name from your list
            prompt=f"necesito  {address}",
            
        )
        return response['response'].strip()
    except ConnectionError as e:
        print(f"Ollama connection failed: {str(e)}")
        return address  # Fallback to original
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return address

def standardize_addresses(df, address_column):
    # Apply LLM-based standardization to each address
    
    df['standardized_address'] = df[address_column].apply(standardize_address_with_llm)
    
    return df

def finalize_standardization(input_csv, output_csv):
    # Load the preprocessed CSV file
    df = pd.read_csv(input_csv)
    
    # Identify the address column (case insensitive)
    address_column = next((col for col in df.columns if 'address' in col.lower()), None)
    if not address_column:
        raise ValueError("No address column found in the dataset.")
    
    # Standardize addresses using the LLM
    df = standardize_addresses(df, address_column)
    
    # Save the final standardized data to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Standardized data saved to {output_csv}")

# Example usage
input_csv = 'preprocessed_addresses.csv'
output_csv = 'final_standardized_addresses.csv'
finalize_standardization(input_csv, output_csv)