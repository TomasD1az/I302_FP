import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def preprocess_binary_categories(df, label):
    df[label] = df[label].apply(
        lambda value: np.nan if pd.isna(value) else str(value).strip().lower()
    )
    df[label] = df[label].apply(
        lambda value: 1 if value in ["sí", "1.0", "1"] else (0 if value in ["no", "0.0", "0"] else np.nan)
    )

def get_binary_plot(df, labels, cols=4):
    n_labels = len(labels)
    rows = n_labels // cols + 1
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
    axes = axes.flatten()

    for i, label in enumerate(labels):
        frequencies = df[label].value_counts(normalize=True, dropna=False) * 100
        categories = ['0', '1', 'NaN (Desconocido)']
        values = [frequencies.get(0, 0), frequencies.get(1, 0), frequencies.get(np.nan, 0)]

        ax = axes[i]
        ax.bar(categories, values, color=['red', 'blue', 'gray'])
        ax.set_title(f'Proporción en {label} (%)')
        ax.set_ylabel('Porcentaje (%)')
        ax.set_xlabel('Categorías')
        ax.set_ylim(0, 100)

        for j, v in enumerate(values):
            ax.text(j, v + 1, f"{v:.2f}%", ha='center')

    for j in range(len(labels), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


#now save this new dataframe in the data folder
#df.to_csv(r'data/alquiler_AMBA_dev_preprocessed.csv', index=False)