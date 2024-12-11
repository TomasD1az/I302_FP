import numpy as np
import pandas as pd

def transform_value(value: int, idu: int, df: pd.DataFrame) -> int:
    """
    Esta función transforma el valor de antigüedad según reglas específicas.
    Se aplica a la columna 'Antiguedad' para manejar valores dentro de un rango determinado, 
    ajustando la lógica según el valor de la antigüedad y la moda de la antigüedad para cada 'id_grid'.
    """

    if 0 <= value <= 145:
        return value
    elif value < 0:
        return 0
    elif pd.isna(value):
        return 0
    elif 145 < value <= 1879:
        mode = df.loc[df['id_grid'] == idu, 'Antiguedad'].mean(skipna=True)
        if mode > 145:
            return 0
        else:
            return mode
    
    elif 1879 < value <= 2024:
        return 2024 - value
    elif 2024 < value <= 2029:
        return 0
    else: #calcular moda (poruqe numeros mas grandes)
        mean = df.loc[df['id_grid'] == idu, 'Antiguedad'].mode()[0]
        if mean > 145:
            return 0
        else:
            return mean
        
def preprocess_category_1(df: pd.DataFrame) -> pd.DataFrame:
    # Hacer triangulacion de valores faltantes (por ahora no hace falta)
    return df
    

def preprocess_category_2(df: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función preprocesa la columna 'Antiguedad' y las columnas de superficie ('SConstrM2', 'STotalM2').
    - Limpia los valores de la columna 'Antiguedad' y los convierte en valores numéricos.
    - Aplica una transformación personalizada a 'Antiguedad' utilizando la función 'transform_value'.
    - Se encarga de reemplazar valores faltantes y negativos por 0 en 'SConstrM2' y 'STotalM2'.
    - Aplica un logaritmo (log1p) a las columnas de superficie para normalizar su distribución.
    - Asegura que 'SConstrM2' no sea mayor que 'STotalM2'.
    """

    df['Antiguedad'] = df['Antiguedad'].str.replace(' años', '')
    df['Antiguedad'] = df['Antiguedad'].str.replace('Hasta ', '')
    df['Antiguedad'] = df['Antiguedad'].astype(str).str.strip()

    df['Antiguedad'] = pd.to_numeric(df['Antiguedad'], errors='coerce')
    df['Antiguedad'] = df['Antiguedad'].fillna(0).astype(int) #los nan los paso a 0

    for idu in df['id_grid'].unique():
        antiguedad_values = df.loc[df['id_grid'] == idu, 'Antiguedad']
        transformed_values = antiguedad_values.apply(lambda x: transform_value(x, idu, df))
        df.loc[df['id_grid'] == idu, 'Antiguedad'] = transformed_values.astype(df['Antiguedad'].dtype)

    df['SConstrM2'] = df['SConstrM2'].apply(lambda x: max(0, x))
    df['STotalM2'] = df['STotalM2'].apply(lambda x: max(0, x))

    df['SConstrM2'] = np.log1p(df['SConstrM2'])
    df['STotalM2'] = np.log1p(df['STotalM2'])

    df['SConstrM2'] = df.apply(lambda row: row['STotalM2'] if row['SConstrM2'] > row['STotalM2'] else row['SConstrM2'], axis=1)
    return df

def preprocess_category_3(df: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función preprocesa las columnas relacionadas con características de la propiedad como 'Dormitorios', 'Banos', 'Ambientes', 'Cocheras' y 'ITE_TIPO_PROD'.
    - Reemplaza valores faltantes por la moda de cada grupo 'id_grid'.
    - Si la moda no está disponible, reemplaza los valores faltantes por la mediana.
    - Aplica logaritmo a las columnas numéricas ('Dormitorios', 'Banos', etc.) para normalizar los valores.
    - Convierte 'ITE_TIPO_PROD' en variables dummy (variables indicadoras).
    """

    columns = ['Dormitorios', 'Banos', 'Ambientes', 'Cocheras', 'ITE_TIPO_PROD']
    
    for col in columns[:-1]:
        modas_por_id = df.groupby('id_grid')[col].agg(lambda x: x.mode()[0] if not x.mode().empty else np.nan)
        df[col] = df.apply(lambda row: modas_por_id[row['id_grid']] if pd.isna(row[col]) else row[col], axis=1)
        
        if df[col].isna().sum() > 0:
            df[col] = df[col].fillna(df[col].median())
    
        df[col] = df[col].apply(lambda x: max(0, x))
        df[col] = np.log1p(df[col])

    df = pd.get_dummies(df, columns=['ITE_TIPO_PROD'], drop_first=False, dtype=int)
    
    return df

def preprocess_category_4(df: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función preprocesa las columnas binarias relacionadas con características adicionales de la propiedad, como 'SalonDeUsosMul', 'Pileta', etc.
    - Convierte los valores 'sí' y 'no' a 1 y 0 respectivamente.
    - En caso de valores faltantes, se reemplazan por la moda de la columna.
    - Los valores de las columnas se convierten a enteros de 8 bits para optimizar el uso de memoria.
    """

    for col in ['SalonDeUsosMul', 'Pileta', 'Gimnasio', 'Laundry', 'Seguridad', 'AccesoInternet', 'Calefaccion', 'AireAC', 'Amoblado']:
    
        df[col] = df[col].apply(lambda value: np.nan if pd.isna(value) else str(value).strip().lower())
        df[col] = df[col].apply(lambda value: 1 if value in ["sí", "1.0", "1"] else (0 if value in ["no", "0.0", "0"] else np.nan))
        
        mode = df[col].mode()[0]
        df[col] = df[col].fillna(mode) 

        df = df.astype({col: 'int8'})
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función aplica todas las transformaciones necesarias al DataFrame de entrada.
    - Elimina columnas no deseadas.
    - Aplica las funciones de preprocesamiento 'preprocess_category_1', 'preprocess_category_2', 'preprocess_category_3' y 'preprocess_category_4'.
    - Filtra los valores de 'precio_pesos_constantes' que sean mayores a 400000.
    - Guarda el DataFrame preprocesado en un archivo CSV.
    """

    categories_to_delete = ["AreaParrillas", "CanchaTennis", "AreaJuegosInfantiles", "BusinessCenter", "PistaJogging", "EstacionamientoVisitas", "SalonFiestas", "Jacuzzi", "Cisterna", "Estacionamiento", "Chimenea", "SistContraIncendios", "Ascensor", "Lobby", "Recepcion", "MesListing", "SitioOrigen", "year", "AreaCine", "LocalesComerciales", "TIPOPROPIEDAD", 'ITE_ADD_CITY_NAME', 'ITE_ADD_STATE_NAME','ITE_ADD_NEIGHBORHOOD_NAME']
    df.drop(columns=categories_to_delete, inplace=True)

    df = preprocess_category_1(df)
    df = preprocess_category_2(df)
    df = preprocess_category_3(df)
    df = preprocess_category_4(df)

    df = df[df['precio_pesos_constantes'] <= 400000]
    df.drop(columns='id_grid', inplace=True)

    df.to_csv(r'data/processed/data_preprocessed.csv', index=False)
    return df