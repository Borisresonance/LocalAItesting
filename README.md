Address standardization is a crucial step in data preprocessing, ensuring that addresses follow a consistent format for better searchability, analytics, and integration with other systems. This project implements two approaches:

LLM-Based Approach: Uses a Large Language Model (LLM) to process and standardize addresses.
NLP-Based Approach: Uses a dictionary-based regex method to replace specific words with their abbreviations.
Each approach has its strengths and weaknesses, which are discussed below.

2️⃣ LLM-Based Approach
Overview
The LLM-based approach uses a Large Language Model (LLM) to interpret and standardize addresses. It relies on AI-generated text transformation to replace certain words in an address with their official abbreviations.

Code Implementation
python
Copy
Edit
import time
import pandas as pd
import ollama
from requests.exceptions import ConnectionError

# LLM Configuration
MODEL_NAME = "deepseek-r1:7b"
MAX_RETRIES = 3
RETRY_DELAY = 2

def standardize_address_with_llm(address):
    system_instruction = """Solo reemplaza estas palabras usando su abreviatura oficial:
    ED=Edificio, P=Piso, CL=Calle, CR=Carrera, DG=Diagonal, AV=Avenida, 
    BL=Bloque, CON=Conjunto, AP=Apartamento, DPTO=Departamento
    Reglas:
    1. Reemplazar solo palabras completas
    2. Conservar números y formato original
    3. Sin explicaciones
    4. Mantener mayúsculas iniciales
    Respuesta solo con la dirección modificada"""
    
    for attempt in range(MAX_RETRIES):
        try:
            response = ollama.generate(
                model=MODEL_NAME,
                prompt=f"Dirección a estandarizar: {address}",
                system=system_instruction,
                options={'temperature': 0.0, 'num_predict': 50}
            )
            return response['response'].strip()
            
        except ConnectionError as e:
            if attempt < MAX_RETRIES - 1:
                print(f"Error de conexión, reintentando ({attempt+1}/{MAX_RETRIES})...")
                time.sleep(RETRY_DELAY)
                continue
            print(f"Error final: {str(e)}")
            return address
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return address

def standardize_addresses(df, address_column):
    df['standardized_address'] = df[address_column].apply(standardize_address_with_llm)
    return df
How It Works
The script calls an LLM (deepseek-r1:7b) to process the address.
The LLM receives a system prompt specifying the rules of transformation.
The response from the LLM is expected to contain only the transformed address.
The function retries up to 3 times in case of a connection failure.
Advantages
✅ Can handle complex variations of address structures.
✅ Can infer abbreviations even if not explicitly listed in rules.
✅ No need for manually created word-replacement dictionaries.

Disadvantages
❌ Unreliable output: The LLM might not always return just the transformed address—it may include reasoning text.
❌ Performance issues: Requires an active LLM server, which can be slow.
❌ Expensive: Requires GPU inference or cloud-based API calls.

When to Use This Approach
When addresses have high variability and cannot be standardized by simple replacements.
When additional context is required (e.g., understanding abbreviations dynamically).
If manual rule maintenance is not feasible.
3️⃣ NLP-Based Approach
Overview
This method replaces specific words with their official abbreviations using a dictionary and regular expressions. It provides consistent, rule-based standardization without relying on AI inference.

Code Implementation
python
Copy
Edit
import re
import pandas as pd
from tqdm import tqdm

# Dictionary of words → abbreviations
ABBREV_MAP = {
    "Edificio": "ED",
    "Piso": "P",
    "Calle": "CL",
    "Carrera": "CR",
    "Diagonal": "DG",
    "Avenida": "AV",
    "Bloque": "BL",
    "Conjunto": "CON",
    "Apartamento": "AP",
    "Departamento": "DPTO"
}

def standardize_address_nlp(address: str) -> str:
    """
    Replaces certain words with their abbreviations.
    - Matches full words only (\b boundaries).
    - Ignores case (re.IGNORECASE).
    - Returns the transformed address.
    """
    if not isinstance(address, str):
        return address  # Return unchanged if NaN or non-string
    
    # Apply replacements using regex
    for original, abbreviation in ABBREV_MAP.items():
        pattern = rf"\b{original}\b"
        address = re.sub(pattern, abbreviation, address, flags=re.IGNORECASE)

    return address

def standardize_addresses(df, address_column):
    tqdm.pandas(desc="Estandarizando direcciones")
    df["standardized_address"] = df[address_column].progress_apply(standardize_address_nlp)
    return df
How It Works
Uses a predefined dictionary of words and their abbreviations.
Uses regex with word boundaries (\b) to ensure only full words are replaced.
Runs in constant time (O(n)) for each address, making it extremely fast and efficient.
Guarantees consistent and predictable transformations.
Advantages
✅ Fast: No external API calls or AI inference.
✅ Deterministic: Always produces the same result for the same input.
✅ Easy to maintain: Just update ABBREV_MAP to modify rules.
✅ Works offline: No need for an AI model.

Disadvantages
❌ Limited to predefined rules: Cannot infer meanings beyond what is defined in ABBREV_MAP.
❌ Does not handle complex restructuring of addresses (e.g., if the format needs to be changed).

When to Use This Approach
When standardization is rule-based and does not require contextual AI reasoning.
When you need a fast and efficient method for processing large datasets.
When you want a simple, maintainable solution without requiring an AI server.
4️⃣ Comparison: LLM vs NLP Approach
Feature	LLM-Based Approach	NLP-Based Approach
Speed	Slow (depends on model)	Very fast
Accuracy	May hallucinate or include reasoning	100% predictable
Maintainability	Needs prompt tuning & retraining	Simple dictionary updates
Infrastructure	Requires GPU / Cloud API	Runs locally
Handles Variability	Can generalize to unseen cases	Limited to predefined words
Final Recommendation
✅ For large-scale, consistent address transformations → Use the NLP-based approach
🤔 For handling unstructured or highly variable input → LLM might be needed
For most structured datasets, the NLP-based method is the best choice, as it is faster, deterministic, and requires no AI inference.

5️⃣ Conclusion
This project implemented two different methods for address standardization:

The LLM-based approach, which is useful for handling complex variations but has unpredictable output.
The NLP-based approach, which is rule-based, fast, and deterministic.
For most cases, the NLP-based approach is the recommended solution unless contextual understanding is necessary.

