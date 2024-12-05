import pandas as pd

df = pd.read_csv(r'data/alquiler_AMBA_dev.csv')
print(df.shape)

def preprocess_binary_categories(label):
    df[label] = df[label].str.replace("Sí", "1", case=False, regex=False)
    df[label] = df[label].str.replace("No", "0", case=False, regex=False)
    df[label] = df[label].str.replace("0.0", "0", case=False, regex=False)
    df[label] = df[label].str.replace("1.0", "1", case=False, regex=False)
    df[label] = df[label].str.strip()

labels = ["Cisterna","AccesoInternet","Calefaccion","AireAC","Estacionamiento","Chimenea","SistContraIncendios"]
for label in labels:
    preprocess_binary_categories(label)
    print(label)
    print(df[label].unique())

#now save this new dataframe in the data folder
df.to_csv(r'data/alquiler_AMBA_dev_preprocessed.csv', index=False)