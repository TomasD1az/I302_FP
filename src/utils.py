import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def preprocess_binary_categories(df, label) -> pd.DataFrame:
    """
    Preprocesa las categorías binarias de una columna específica en el DataFrame
    La columna `label` será procesada para que sus valores "sí", "1.0", "1" sean convertidos a 1,
    y los valores "no", "0.0", "0" serán convertidos a 0. Los valores restantes serán NaN.
    """
    
    df[label] = df[label].apply(
        lambda value: np.nan if pd.isna(value) else str(value).strip().lower()
    )

    df[label] = df[label].apply(
        lambda value: 1 if value in ["sí", "1.0", "1"] else (0 if value in ["no", "0.0", "0"] else np.nan)
    )
    return df


def fill_with_mode(df: pd.DataFrame, label: list) -> pd.DataFrame:
    """
    Rellena los valores faltantes de la columna `label` con la moda de esa columna.
    Si hay valores NaN en la columna, serán reemplazados por el valor que más se repite.
    """

    mode = df[label].mode()[0]
    df[label] = df[label].fillna(mode)
    return df

def get_binary_plot(df: pd.DataFrame, labels: list, cols=4) -> None:
    """
    Genera un gráfico de barras que muestra la distribución de valores binarios (0, 1 y NaN) para múltiples columnas.
    Cada columna especificada en `labels` será representada en su propio gráfico, con barras de color rojo para 0, azul para 1
    y gris para los valores NaN.
    """
        
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