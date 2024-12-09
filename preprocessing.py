import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def fill_with_mode_id(df, label):
    modas_por_id = df.groupby('id_grid')[label].agg(lambda x: x.mode()[0] if not x.mode().empty else np.nan)
    df[label] = df.apply(lambda row: modas_por_id[row['id_grid']] if pd.isna(row[label]) else row[label], axis=1)

    #Si por laguna razon falla la moda, usamos la mediana general
    if df[label].isna().sum() > 0:
        df[label] = df[label].fillna(df[label].median())
    return df

def transform_value(value, idu, df):
        if 0 <= value <= 145:
            return value
        elif value < 0:
            return 0
        elif pd.isna(value):
            return 0
        elif 145 < value <= 1879:
            #return moda de la antiguedad, si es mas que 145, ponemos 0
            mode = df.loc[data['id_grid'] == idu, 'Antiguedad'].mean(skipna=True)
            if mode > 145:
                return 0
            else:
                return mode
        
        elif 1879 < value <= 2024:
            return 2024 - value
        elif 2024 < value <= 2029:
            return 0
        else:  # value > 2029
            #calcular moda (poruqe numeros mas grandes), si es mas que 145, ponemos 0
            mean = df.loc[data['id_grid'] == idu, 'Antiguedad'].mode()[0]
            if mean > 145:
                return 0
            else:
                return mean

def preprocess_antiguedad(df):
    df['Antiguedad'] = df['Antiguedad'].str.replace(' años', '')
    df['Antiguedad'] = df['Antiguedad'].str.replace('Hasta ', '')
    df['Antiguedad'] = df['Antiguedad'].astype(str).str.strip()

    #pasarlo a int
    df['Antiguedad'] = pd.to_numeric(df['Antiguedad'], errors='coerce')
    df['Antiguedad'] = df['Antiguedad'].fillna(0).astype(int) #los nan los paso a 0

    for idu in df['id_grid'].unique():
        antiguedad_values = df.loc[df['id_grid'] == idu, 'Antiguedad']
        transformed_values = antiguedad_values.apply(lambda x: transform_value(x, idu, df))
        df.loc[df['id_grid'] == idu, 'Antiguedad'] = transformed_values.astype(df['Antiguedad'].dtype)

    return df

def preprocess_ConstrM2_TotalM2(df):
    # En caso que alguna sea Nan o negativa, se reemplaza por 0
    df['SConstrM2'] = df['SConstrM2'].apply(lambda x: max(0, x))
    df['STotalM2'] = df['STotalM2'].apply(lambda x: max(0, x))

    #Ahora hago una tranformacion de estas variables para que los outliers no tengan tanto impacto
    df['SConstrM2'] = np.log1p(df['SConstrM2'])
    df['STotalM2'] = np.log1p(df['STotalM2'])

    # hago que cualquier valor que tenga ConstrM2 mayor que TotalM2, los pongo iguales
    df['SConstrM2'] = df.apply(lambda row: row['STotalM2'] if row['SConstrM2'] > row['STotalM2'] else row['SConstrM2'], axis=1)
    return df

def preprocess_catehory_3(df):
    for col in ['Dormitorios', 'Banos', 'Ambientes', 'Cocheras','ITE_TIPO_PROD']:
        df = fill_with_mode_id(df, col)

    # En caso que alguna sea Nan o negativa, se reemplaza por 0
    df['Dormitorios'] = df['Dormitorios'].apply(lambda x: max(0, x))
    data['Banos'] = data['Banos'].apply(lambda x: max(0, x))
    data['Ambientes'] = data['Ambientes'].apply(lambda x: max(0, x))
    data['Cocheras'] = data['Cocheras'].apply(lambda x: max(0, x))

    #Ahora hago una tranformacion de estas variables para que los outliers no tengan tanto impacto
    df['Dormitorios'] = np.log1p(df['Dormitorios'])
    df['Banos'] = np.log1p(df['Banos'])
    df['Ambientes'] = np.log1p(df['Ambientes'])
    df['Cocheras'] = np.log1p(df['Cocheras'])
    df = pd.get_dummies(df, columns=['ITE_TIPO_PROD'], drop_first=False, dtype=int)
    return df

def preprocess_category_4(df):
    for col in ['SalonDeUsosMul', 'Pileta', 'Gimnasio', 'Laundry', 'Seguridad', 'AccesoInternet', 'Calefaccion', 'AireAC', 'Amoblado']:
        df = preprocess_binary_categories(df, col)
    return df

def preprocess_binary_categories(df, label):
    df[label] = df[label].apply(
        lambda value: np.nan if pd.isna(value) else str(value).strip().lower()
    )

    df[label] = df[label].apply(
        lambda value: 1 if value in ["sí", "1.0", "1"] else (0 if value in ["no", "0.0", "0"] else np.nan)
    )
    
    mode = df[label].mode()[0]
    df[label] = df[label].fillna(mode) 

    df = df.astype({label: 'int8'})
    return df


# Load the dataset
data = pd.read_csv(r'data/alquiler_AMBA_dev.csv')
print(data.shape)
categories_to_delete = ["AreaParrillas", "CanchaTennis", "AreaJuegosInfantiles", "BusinessCenter", "PistaJogging", "EstacionamientoVisitas", "SalonFiestas", "Jacuzzi", "Cisterna", "Estacionamiento", "Chimenea", "SistContraIncendios", "Ascensor", "Lobby", "Recepcion", "MesListing", "SitioOrigen", "year", "AreaCine", "LocalesComerciales", "TIPOPROPIEDAD", 'ITE_ADD_CITY_NAME', 'ITE_ADD_STATE_NAME','ITE_ADD_NEIGHBORHOOD_NAME']
data.drop(columns=categories_to_delete, inplace=True)
print(data.shape)

data = preprocess_ConstrM2_TotalM2(data)
data = preprocess_antiguedad(data)
data = preprocess_catehory_3(data)
data = preprocess_category_4(data)

data = data[data['precio_pesos_constantes'] <= 400000]
data.drop(columns='id_grid', inplace=True)

#now save this new dataframe in the data folder
data.to_csv(r'data/data_preprocessed.csv', index=False)