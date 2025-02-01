import re
import pandas as pd
from tqdm import tqdm

# Diccionario de palabras → abreviaturas
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
    Reemplaza ciertas palabras con sus abreviaturas oficiales.
    - Coincide palabras completas (usando boundaries \b).
    - Ignora mayúsculas/minúsculas (flags=re.IGNORECASE).
    - Retorna la dirección transformada.
    """
    if not isinstance(address, str):
        # Si hay valores NaN o no string, devuélvelos tal cual
        return address

    # Reemplaza cada palabra usando el diccionario
    for original, abbreviation in ABBREV_MAP.items():
        # \b para coincidir con límites de palabra, re.IGNORECASE para ignorar mayúsculas
        pattern = rf"\b{original}\b"
        address = re.sub(pattern, abbreviation, address, flags=re.IGNORECASE)

    return address


def standardize_addresses(df, address_column):
    """
    Aplica la función de estandarización a cada fila de la columna de direcciones.
    Usamos 'progress_apply' para tener una barra de progreso.
    """
    tqdm.pandas(desc="Estandarizando direcciones")
    df["standardized_address"] = df[address_column].progress_apply(standardize_address_nlp)
    return df


def finalize_standardization(input_csv, output_csv):
    """
    1. Lee el CSV.
    2. Busca una columna con 'address' en su nombre.
    3. Estandariza direcciones usando la función NLP.
    4. Guarda el resultado a un nuevo CSV.
    """
    try:
        df = pd.read_csv(input_csv)
        
        # Buscar la columna 'address' (ignorando mayúsculas/minúsculas)
        address_column = next((col for col in df.columns if 'address' in col.lower()), None)
        if not address_column:
            raise ValueError("No se encontró ninguna columna con la palabra 'address'.")
        
        # Estandarizar direcciones en esa columna
        df = standardize_addresses(df, address_column)
        
        # Guardar en CSV
        df.to_csv(output_csv, index=False)
        print(f"✅ Datos guardados en: {output_csv}")
        return True
    
    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
        return False


if __name__ == "__main__":
    # Nombres de archivos de entrada y salida
    input_csv = "preprocessed_addresses.csv"
    output_csv = "final_standardized_addresses.csv"
    
    if finalize_standardization(input_csv, output_csv):
        print("Proceso completado exitosamente")
    else:
        print("El proceso encontró errores")
